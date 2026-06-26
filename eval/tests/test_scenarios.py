from pathlib import Path
from eval.harness.scenarios import parse_scenarios, Scenario

FIXTURE = Path(__file__).parent / "fixtures" / "sample-skill.md"


def test_parses_two_scenarios():
    scenarios = parse_scenarios(FIXTURE)
    assert len(scenarios) == 2
    assert all(isinstance(s, Scenario) for s in scenarios)


def test_live_scenario_fields():
    s = parse_scenarios(FIXTURE)[0]
    assert s.id == "scenario-1"
    assert s.mode == "live"
    assert s.prompt == "/audit-deal Planity France"
    assert s.deal_crm_id == "006MI00000toSpRYAU"
    assert {"deal_status": ["Open"]} in s.predicates
    assert {"no_contact_role": "Champion"} in s.predicates
    assert any("verdict line" in e for e in s.expected)
    assert any("Invent a champion" in a for a in s.anti)
    assert any("verdict line at the top" in m for m in s.must_haves)


def test_synthetic_scenario_fields():
    s = parse_scenarios(FIXTURE)[1]
    assert s.mode == "synthetic"
    assert s.deal_crm_id is None
    assert "EUR80k" in s.synthetic_context
    assert s.predicates == []
