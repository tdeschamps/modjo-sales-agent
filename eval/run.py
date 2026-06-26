"""CLI entrypoint + per-scenario orchestration for the Modjo Sales Agent eval harness."""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path

from eval.harness.scenarios import parse_scenarios
from eval.harness.runner import invoke as default_invoke
from eval.harness.judge import grade as default_grade, VerdictError
from eval.harness.scanner import scan
from eval.harness.fixtures import check_predicates
from eval.harness.verdict import decide_status
from eval.harness.report import RunRecord, write_run, append_summary, dimension_rates, print_table

_ROOT = Path(__file__).resolve().parent
_SCENARIOS = _ROOT / "scenarios"
_RUBRIC = (_ROOT / "rubric.md")
TRUST_CRITICAL = {"audit-this-deal:scenario-7", "coach-this-rep:scenario-2",
                  "score-this-call:scenario-5", "prep-this-meeting:scenario-6",
                  "learn-from-closed-deals:scenario-6"}


def _scanner_summary(scan_res) -> str:
    if scan_res.skipped_no_oracle:
        return "scanner skipped (no Modjo returns — synthetic or no-tool run)"
    if scan_res.anti_fab_fail:
        return "FABRICATION DETECTED: " + "; ".join(scan_res.findings)
    return "no fabrication detected by deterministic scanner"


def _fetch_deal(crm_id: str) -> dict:
    """Minimal read-only MCP query to refetch a deal for predicate revalidation."""
    prompt = (
        f"Call mcp__modjo__get_deals filtered to crmId {crm_id} (or name match) and "
        "return ONLY the single deal object as compact JSON with keys "
        "status, amount, contacts (name+role), call_count. No prose."
    )
    proc = subprocess.run(
        ["claude", "-p", prompt, "--output-format", "json", "--model", "haiku"],
        capture_output=True, text=True, timeout=120, check=False,
    )
    try:
        envelope = json.loads(proc.stdout)
        result = envelope.get("result", proc.stdout)
        start, end = result.find("{"), result.rfind("}")
        return json.loads(result[start:end + 1])
    except Exception:
        return {}


def run_scenario(skill, scenario, runs_idx, model, rubric,
                 invoke=None, grade=None, fetch_deal=None) -> RunRecord:
    invoke = invoke or default_invoke
    grade = grade or default_grade
    fetch_deal = fetch_deal or _fetch_deal

    base = RunRecord(skill=skill, scenario_id=scenario.id, run=runs_idx, mode=scenario.mode,
                     status="ERROR", verdict=None, dimensions={}, aggregate=None,
                     cost_usd=None, session_id=None)

    if scenario.mode == "live" and scenario.predicates:
        deal = fetch_deal(scenario.deal_crm_id)
        ok, reason = check_predicates(scenario.predicates, deal)
        if not ok:
            base.status = "FIXTURE_STALE"
            base.scanner_findings = [f"fixture drift: {reason}"]
            return base

    rr = invoke(scenario, model)
    base.session_id = rr.trace.session_id
    base.cost_usd = rr.trace.cost_usd
    if rr.status != "OK":
        base.status = "ERROR"
        base.scanner_findings = [f"runner error: {rr.stderr[:200]}"]
        return base

    scan_res = scan(rr.trace, scenario.forbidden_entities)
    base.scanner_findings = scan_res.findings

    ground_truth = rr.trace.modjo_returns_text()
    try:
        verdict = grade(skill=skill, scenario=scenario, output=rr.trace.output,
                        ground_truth=ground_truth, scanner_summary=_scanner_summary(scan_res),
                        rubric=rubric, model=model)
    except VerdictError as e:
        base.status = "JUDGE_ERROR"
        base.scanner_findings.append(f"judge: {e}")
        return base

    base.dimensions = verdict.dimensions
    base.aggregate = verdict.aggregate
    base.status = decide_status(
        run_status="OK", scanner_anti_fab=scan_res.anti_fab_fail,
        judge_verdict=verdict.verdict, dimensions=verdict.dimensions,
        aggregate=verdict.aggregate, mode=scenario.mode,
    )
    base.verdict = verdict.verdict
    return base


def main(argv=None):
    p = argparse.ArgumentParser(description="Run Modjo Sales Agent eval scenarios.")
    p.add_argument("skill", help="skill name, e.g. audit-this-deal")
    p.add_argument("--scenario", type=int, help="single scenario number (1-based)")
    p.add_argument("--runs", type=int, default=None, help="runs per scenario")
    p.add_argument("--judge-model", default="opus")
    p.add_argument("--invoke-model", default="opus")
    p.add_argument("--results", default=None, help="results dir")
    args = p.parse_args(argv)

    if not _cli_present():
        print("ERROR: `claude` CLI not found on PATH. Install it and retry.", file=sys.stderr)
        return 2

    scen_file = _SCENARIOS / f"{args.skill}.md"
    if not scen_file.exists():
        print(f"ERROR: no scenario file at {scen_file}", file=sys.stderr)
        return 2
    scenarios = parse_scenarios(scen_file)
    if args.scenario:
        scenarios = [s for s in scenarios if s.id == f"scenario-{args.scenario}"]

    rubric = _RUBRIC.read_text()
    results_dir = Path(args.results) if args.results else _ROOT / "results" / _today()
    results_dir.mkdir(parents=True, exist_ok=True)

    records = []
    for scenario in scenarios:
        key = f"{args.skill}:{scenario.id}"
        n_runs = args.runs or (5 if key in TRUST_CRITICAL else 3)
        for i in range(1, n_runs + 1):
            rec = run_scenario(args.skill, scenario, i, args.invoke_model, rubric)
            rec.cli_version = _cli_version()
            write_run(results_dir, rec)
            append_summary(results_dir, rec)
            records.append(rec)
            print(f"  {scenario.id} run {i}/{n_runs}: {rec.status}")

    print_table(records)
    rates = dimension_rates(records)
    print("\nPer-dimension failures:")
    for dim, r in rates.items():
        if r["total"]:
            print(f"  {dim:<18} {r['fail_count']}/{r['total']}")

    failed = [r for r in records if r.status != "PASS"]
    print(f"\nResults written to {results_dir}")
    return 0 if not failed else 1


def _cli_present() -> bool:
    from shutil import which
    return which("claude") is not None


def _cli_version() -> str:
    try:
        return subprocess.run(["claude", "--version"], capture_output=True, text=True,
                              timeout=30, check=False).stdout.strip()
    except Exception:
        return "unknown"


def _today() -> str:
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")


if __name__ == "__main__":
    raise SystemExit(main())
