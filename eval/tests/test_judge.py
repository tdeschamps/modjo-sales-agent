from eval.harness.judge import build_judge_prompt, parse_verdict, Verdict, VerdictError
from eval.harness.scenarios import Scenario


def _scn():
    return Scenario(
        id="scenario-1", title="t", mode="live", prompt="/audit-deal X",
        deal_crm_id="006X", expects_shape="", predicates=[],
        synthetic_context=None,
        expected=["Lead with verdict"], anti=["Invent a champion"],
        must_haves=["verdict line at top"],
    )


def test_prompt_fills_all_placeholders():
    p = build_judge_prompt(
        skill="audit-this-deal", scenario=_scn(),
        output="Verdict: ...", ground_truth='{"contacts":[]}',
        scanner_summary="no fabrication detected", rubric="RUBRIC TEXT",
    )
    assert "audit-this-deal" in p
    assert "Invent a champion" in p
    assert '{"contacts":[]}' in p
    assert "no fabrication detected" in p
    assert "RUBRIC TEXT" in p
    assert "{GROUND_TRUTH}" not in p


def test_parse_valid_json_verdict():
    raw = '''Sure, here is my grade:
    {"specificity":{"score":2,"reason":"r","quote_if_fail":""},
     "anti_fabrication":{"score":2,"reason":"r","quote_if_fail":""},
     "action_quality":{"score":2,"reason":"r","quote_if_fail":""},
     "honesty":{"score":2,"reason":"r","quote_if_fail":""},
     "structure":{"score":1,"reason":"r","quote_if_fail":""},
     "skill_specific":{"score":2,"reason":"r","quote_if_fail":""},
     "aggregate":11,"verdict":"PASS","anti_patterns_observed":[],
     "top_coaching_note":"tighten structure"}'''
    v = parse_verdict(raw)
    assert isinstance(v, Verdict)
    assert v.verdict == "PASS"
    assert v.dimensions["structure"]["score"] == 1
    assert v.aggregate == 11


def test_parse_rejects_bad_enum():
    raw = '{"verdict":"MAYBE"}'
    try:
        parse_verdict(raw)
        assert False, "should have raised"
    except VerdictError:
        pass
