"""Deterministic anti-fabrication scan: load-bearing named claims must appear in the
captured Modjo returns (the ground-truth oracle). Conservative — flags only
high-confidence fabrications (a named role assignment or an explicit forbidden entity)."""
from __future__ import annotations
import re
from dataclasses import dataclass, field
from .trace import Trace

_ROLE_WORDS = r"(?i:champion|economic buyer|decision maker|economic-buyer|decision-maker)"
_NAME = r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})"
_PATTERNS = [
    re.compile(_ROLE_WORDS + r"\s*[:\-]?\s*(?:is\s+)?" + _NAME),
    re.compile(_NAME + r"\s+is\s+the\s+" + _ROLE_WORDS),
]


@dataclass
class ScanResult:
    anti_fab_fail: bool = False
    skipped_no_oracle: bool = False
    findings: list[str] = field(default_factory=list)


def _candidate_names(output: str) -> set[str]:
    names: set[str] = set()
    for pat in _PATTERNS:
        for m in pat.finditer(output):
            names.add(m.group(1))
    return names


def scan(trace: Trace, forbidden_entities: list[str]) -> ScanResult:
    res = ScanResult()
    oracle = trace.modjo_returns_text()

    for ent in forbidden_entities:
        if re.search(re.escape(ent), trace.output, re.IGNORECASE):
            res.anti_fab_fail = True
            res.findings.append(f"forbidden entity present in output: {ent!r}")

    if not oracle.strip():
        res.skipped_no_oracle = True
        return res

    for name in _candidate_names(trace.output):
        if not re.search(re.escape(name), oracle, re.IGNORECASE):
            res.anti_fab_fail = True
            res.findings.append(
                f"named role-holder {name!r} not present in any Modjo return"
            )
    return res
