"""Invoke a skill via the real `claude` CLI (headless), capture the stream-json trace."""
from __future__ import annotations
import subprocess
from dataclasses import dataclass
from .scenarios import Scenario
from .trace import parse_stream, Trace

DEFAULT_TIMEOUT = 540  # heavy skills (multi-agent-call) run ~125-200s; serial batches slow later runs — give headroom


@dataclass
class RunResult:
    status: str
    trace: Trace
    stderr: str = ""
    attempts: int = 1


from pathlib import Path

# The plugin must be loaded into the headless session and its slash commands
# referenced with the plugin-name prefix, else `claude -p "/audit-deal"` returns
# "Unknown command" (verified 2026-06-04). bypassPermissions lets the read-only
# Modjo MCP calls run without an interactive prompt that headless mode can't answer.
PLUGIN_NAME = "modjo-sales-agent"
PLUGIN_DIR = str(Path(__file__).resolve().parents[1].parent)


def build_argv(prompt: str, model: str) -> list[str]:
    return [
        "claude", "-p", prompt,
        "--output-format", "stream-json",
        "--verbose",
        "--model", model,
        "--plugin-dir", PLUGIN_DIR,
        "--permission-mode", "bypassPermissions",
    ]


def _namespace_command(prompt: str) -> str:
    # "/audit-deal X" -> "/modjo-sales-agent:audit-deal X"; leave non-slash prompts alone.
    if prompt.startswith("/") and not prompt.startswith(f"/{PLUGIN_NAME}:"):
        return f"/{PLUGIN_NAME}:" + prompt[1:]
    return prompt


def build_prompt(scenario: Scenario) -> str:
    prompt = _namespace_command(scenario.prompt)
    if scenario.mode == "synthetic" and scenario.synthetic_context:
        return (
            f"{prompt}\n\n"
            "--- GIVEN STATE (treat as the Modjo data for this run) ---\n"
            f"{scenario.synthetic_context}\n"
            "--- END GIVEN STATE ---"
        )
    return prompt


def _default_runner(argv: list[str], timeout: int):
    proc = subprocess.run(
        argv, capture_output=True, text=True, timeout=timeout, check=False,
    )
    return proc.returncode, proc.stdout, proc.stderr


def invoke(scenario: Scenario, model: str = "opus", runner=_default_runner,
           timeout: int = DEFAULT_TIMEOUT) -> RunResult:
    argv = build_argv(build_prompt(scenario), model)
    last_stderr = ""
    stdout = ""
    for attempt in (1, 2):
        try:
            rc, stdout, stderr = runner(argv, timeout)
        except subprocess.TimeoutExpired:
            rc, stdout, stderr = 124, "", "timeout"
        last_stderr = stderr
        trace = parse_stream(stdout)
        infra_fail = rc != 0 or trace.is_error or trace.raw_lines == 0
        if not infra_fail:
            return RunResult(status="OK", trace=trace, stderr=stderr, attempts=attempt)
    return RunResult(status="ERROR", trace=parse_stream(stdout),
                     stderr=last_stderr, attempts=2)
