"""Persist per-run JSON + a summary CSV with per-dimension failure rates."""
from __future__ import annotations
import csv
import json
from dataclasses import dataclass, field, asdict
from pathlib import Path

_DIMS = ["specificity", "anti_fabrication", "action_quality", "honesty", "structure", "skill_specific"]


@dataclass
class RunRecord:
    skill: str
    scenario_id: str
    run: int
    mode: str
    status: str
    verdict: str | None
    dimensions: dict
    aggregate: int | None
    cost_usd: float | None
    session_id: str | None
    scanner_findings: list = field(default_factory=list)
    cli_version: str = ""


def write_run(results_dir: Path, rec: RunRecord) -> Path:
    out = Path(results_dir) / rec.skill
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{rec.scenario_id}-run{rec.run}.json"
    path.write_text(json.dumps(asdict(rec), indent=2))
    return path


def append_summary(results_dir: Path, rec: RunRecord) -> Path:
    path = Path(results_dir) / "summary.csv"
    fields = ["skill", "scenario_id", "run", "mode", "status", "verdict",
              "aggregate", "cost_usd"] + _DIMS
    exists = path.exists()
    with path.open("a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        if not exists:
            w.writeheader()
        row = {k: getattr(rec, k, "") for k in
               ["skill", "scenario_id", "run", "mode", "status", "verdict", "aggregate", "cost_usd"]}
        for d in _DIMS:
            row[d] = (rec.dimensions.get(d, {}) or {}).get("score", "")
        w.writerow(row)
    return path


def dimension_rates(records: list[RunRecord]) -> dict:
    rates = {d: {"fail_count": 0, "total": 0} for d in _DIMS}
    for rec in records:
        for d in _DIMS:
            score = (rec.dimensions.get(d, {}) or {}).get("score")
            if score is None:
                continue
            rates[d]["total"] += 1
            if score == 0:
                rates[d]["fail_count"] += 1
    return rates


def print_table(records: list[RunRecord]) -> None:
    by_scenario: dict[str, list[RunRecord]] = {}
    for r in records:
        by_scenario.setdefault(r.scenario_id, []).append(r)
    print(f"\n{'scenario':<16}{'runs':<6}{'pass':<6}{'result':<14}")
    print("-" * 42)
    for sid, recs in sorted(by_scenario.items()):
        passes = sum(1 for r in recs if r.status == "PASS")
        # Trust-critical rule: a scenario passes ONLY if every run passed.
        # Otherwise show FAIL with the failing run's status, never the first run's.
        if recs and passes == len(recs):
            overall = "PASS"
        else:
            failed = [r for r in recs if r.status != "PASS"]
            overall = f"FAIL ({failed[0].status})" if failed else "FAIL"
        print(f"{sid:<16}{len(recs):<6}{passes:<6}{overall:<14}")
