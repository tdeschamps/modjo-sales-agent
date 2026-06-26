import csv
import json
from eval.harness.report import RunRecord, write_run, append_summary, dimension_rates


def _rec(status="PASS", verdict="PASS", scenario="scenario-1", run=1):
    return RunRecord(
        skill="audit-this-deal", scenario_id=scenario, run=run, mode="live",
        status=status, verdict=verdict,
        dimensions={"anti_fabrication": {"score": 2}, "structure": {"score": 1}},
        aggregate=11, cost_usd=0.1, session_id="s1", scanner_findings=[],
    )


def test_write_run_creates_json(tmp_path):
    path = write_run(tmp_path, _rec())
    assert path.exists()
    data = json.loads(path.read_text())
    assert data["scenario_id"] == "scenario-1"
    assert data["status"] == "PASS"


def test_append_summary_writes_csv_row(tmp_path):
    csv_path = append_summary(tmp_path, _rec())
    rows = list(csv.DictReader(csv_path.open()))
    assert rows[0]["skill"] == "audit-this-deal"
    assert rows[0]["status"] == "PASS"
    assert rows[0]["anti_fabrication"] == "2"


def test_dimension_rates_counts_failures():
    recs = [_rec(), _rec(run=2)]
    recs[1].dimensions["structure"]["score"] = 0
    rates = dimension_rates(recs)
    assert rates["structure"]["fail_count"] == 1
    assert rates["anti_fabrication"]["fail_count"] == 0
