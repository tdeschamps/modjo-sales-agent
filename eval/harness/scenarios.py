"""Parse eval/scenarios/<skill>.md into Scenario objects (prose + FIXTURE)."""
from __future__ import annotations
import re
from dataclasses import dataclass, field
from pathlib import Path
import yaml

_FIXTURE_RE = re.compile(r"<!--\s*FIXTURE\s*\n(.*?)\n-->", re.DOTALL)


@dataclass
class Scenario:
    id: str
    title: str
    mode: str                       # "live" | "synthetic"
    prompt: str
    deal_crm_id: str | None
    expects_shape: str
    predicates: list[dict]
    synthetic_context: str | None
    expected: list[str]
    anti: list[str]
    must_haves: list[str]
    forbidden_entities: list[str] = field(default_factory=list)


def _extract_bullets(section: str) -> list[str]:
    return [
        line.lstrip("-* ").strip()
        for line in section.splitlines()
        if line.strip().startswith(("-", "*"))
    ]


def _section(body: str, header_substr: str) -> str:
    """Return text under a bolded header like **Expected behaviors ...** up to next blank-line block break."""
    pattern = re.compile(
        r"\*\*[^*]*" + re.escape(header_substr) + r"[^*]*\*\*:?\s*\n(.*?)(?=\n\*\*|\n##|\Z)",
        re.DOTALL | re.IGNORECASE,
    )
    m = pattern.search(body)
    return m.group(1) if m else ""


def parse_scenarios(path: Path) -> list[Scenario]:
    text = Path(path).read_text()

    must_block = _section_by_heading(text, "Skill-specific must-haves")
    global_must = _extract_bullets(must_block)

    scenarios: list[Scenario] = []
    blocks = re.split(r"\n##\s+Scenario\s+", text)
    for idx, block in enumerate(blocks[1:], start=1):
        title_line = block.splitlines()[0].strip()
        fixture_m = _FIXTURE_RE.search(block)
        if not fixture_m:
            continue
        fx = yaml.safe_load(fixture_m.group(1)) or {}
        scenarios.append(
            Scenario(
                id=f"scenario-{idx}",
                title=title_line,
                mode=fx.get("mode", "live"),
                prompt=fx["prompt"],
                deal_crm_id=fx.get("deal_crmId"),
                expects_shape=fx.get("expects_shape", ""),
                predicates=fx.get("predicates") or [],
                synthetic_context=fx.get("synthetic_context"),
                expected=_extract_bullets(_section(block, "Expected behaviors")),
                anti=_extract_bullets(_section(block, "Anti-behaviors")),
                must_haves=list(global_must),
                forbidden_entities=fx.get("forbidden_entities") or [],
            )
        )
    return scenarios


def _section_by_heading(text: str, heading_substr: str) -> str:
    pattern = re.compile(
        r"##\s+[^\n]*" + re.escape(heading_substr) + r"[^\n]*\n(.*?)(?=\n##|\Z)",
        re.DOTALL | re.IGNORECASE,
    )
    m = pattern.search(text)
    return m.group(1) if m else ""
