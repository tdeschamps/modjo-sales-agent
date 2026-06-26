"""Build the judge prompt, run an isolated `claude -p`, validate the JSON verdict."""
from __future__ import annotations
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
import jsonschema
from .scenarios import Scenario
from .trace import parse_stream

_TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "judge-prompt.md"
_DIMS = ["specificity", "anti_fabrication", "action_quality", "honesty", "structure", "skill_specific"]

_DIM_SCHEMA = {
    "type": "object",
    "properties": {
        "score": {"type": "integer", "enum": [0, 1, 2]},
        "reason": {"type": "string"},
        "quote_if_fail": {"type": "string"},
    },
    "required": ["score"],
}
_VERDICT_SCHEMA = {
    "type": "object",
    "properties": {
        **{d: _DIM_SCHEMA for d in _DIMS},
        "aggregate": {"type": "integer", "minimum": 0, "maximum": 12},
        "verdict": {"type": "string", "enum": ["PASS", "FAIL"]},
        "anti_patterns_observed": {"type": "array", "items": {"type": "string"}},
        "top_coaching_note": {"type": "string"},
    },
    "required": _DIMS + ["aggregate", "verdict"],
    "additionalProperties": True,
}


class VerdictError(Exception):
    pass


@dataclass
class Verdict:
    dimensions: dict
    aggregate: int
    verdict: str
    anti_patterns_observed: list
    top_coaching_note: str
    raw: str


def _extract_template_body() -> str:
    text = _TEMPLATE_PATH.read_text()
    m = re.search(r"## The prompt template\s*\n```(.*?)```", text, re.DOTALL)
    return m.group(1) if m else text


def build_judge_prompt(skill, scenario: Scenario, output, ground_truth,
                       scanner_summary, rubric) -> str:
    body = _extract_template_body()
    scenario_block = (
        f"Title: {scenario.title}\nPrompt: {scenario.prompt}\n"
        f"Expected (MUST): {scenario.expected}\n"
        f"Anti (MUST NOT): {scenario.anti}\n"
        f"Must-haves: {scenario.must_haves}"
    )
    repl = {
        "{SKILL_NAME}": skill,
        "{SCENARIO_BLOCK}": scenario_block,
        "{PLUGIN_OUTPUT}": output,
        "{GROUND_TRUTH}": ground_truth or "(no Modjo returns captured)",
        "{SCANNER_RESULT}": scanner_summary,
        "{RUBRIC}": rubric,
    }
    for k, v in repl.items():
        body = body.replace(k, str(v))
    return body


def _candidate_json_objects(raw: str):
    """Yield every balanced {...} substring (handles JSON buried in prose preamble)."""
    # Prefer a fenced ```json block if present.
    fenced = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL)
    for f in fenced:
        yield f
    depth = 0
    start = None
    for i, ch in enumerate(raw):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            if depth > 0:
                depth -= 1
                if depth == 0 and start is not None:
                    yield raw[start:i + 1]
                    start = None


def parse_verdict(raw: str) -> Verdict:
    data = None
    for candidate in _candidate_json_objects(raw):
        try:
            obj = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and "verdict" in obj:
            data = obj
            break
    if data is None:
        raise VerdictError("no JSON object with a verdict key found in judge output")
    try:
        jsonschema.validate(data, _VERDICT_SCHEMA)
    except jsonschema.ValidationError as e:
        raise VerdictError(f"schema violation: {e.message}") from e
    return Verdict(
        dimensions={d: data[d] for d in _DIMS},
        aggregate=data["aggregate"],
        verdict=data["verdict"],
        anti_patterns_observed=data.get("anti_patterns_observed", []),
        top_coaching_note=data.get("top_coaching_note", ""),
        raw=raw,
    )


def _judge_argv(prompt: str, model: str) -> list[str]:
    return [
        "claude", "-p", prompt,
        "--output-format", "json",
        "--model", model,
        # Empty-but-valid MCP set isolates the judge from all tools/live data.
        # A bare "{}" is rejected by the CLI ("expected record"); needs mcpServers key.
        "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
    ]


def grade(skill, scenario, output, ground_truth, scanner_summary, rubric,
          model="opus", runner=None, timeout=300) -> Verdict:
    prompt = build_judge_prompt(skill, scenario, output, ground_truth, scanner_summary, rubric)
    argv = _judge_argv(prompt, model)

    def _run(argv, timeout):
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=timeout, check=False)
        return proc.stdout
    run = runner or _run

    last_err = None
    for _ in (1, 2):
        stdout = run(argv, timeout)
        text = _unwrap_result(stdout)
        try:
            return parse_verdict(text)
        except VerdictError as e:
            last_err = e
    raise VerdictError(f"judge output unparseable after retry: {last_err}")


def _unwrap_result(stdout: str) -> str:
    """`claude --output-format json` returns one envelope; the model reply is in .result.
    Fall back to raw stdout if it's not a recognizable envelope (e.g. test injects raw text)."""
    try:
        env = json.loads(stdout)
        if isinstance(env, dict) and "result" in env:
            return env["result"]
    except (json.JSONDecodeError, TypeError):
        pass
    return stdout
