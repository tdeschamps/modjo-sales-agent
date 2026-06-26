from eval.harness.scenarios import Scenario
from eval.harness.trace import Trace, ToolCall
from eval.harness.judge import Verdict
from eval.run import run_scenario


def _scn(mode="live", **kw):
    base = dict(
        id="scenario-1", title="t", mode=mode, prompt="/audit-deal X",
        deal_crm_id="006X", expects_shape="", predicates=[],
        synthetic_context=None, expected=[], anti=[], must_haves=[],
    )
    base.update(kw)
    return Scenario(**base)


def _trace(output, champion_in_returns):
    t = Trace(output=output, is_error=False, session_id="s1", cost_usd=0.1)
    returns = '{"contacts":[{"name":"Alice","role":"Champion"}]}' if champion_in_returns else '{"contacts":[]}'
    t.tool_calls.append(ToolCall("mcp__modjo__get_deals", {}, returns))
    return t


def _pass_verdict():
    dims = {d: {"score": 2} for d in
            ["specificity", "anti_fabrication", "action_quality", "honesty", "structure", "skill_specific"]}
    return Verdict(dimensions=dims, aggregate=12, verdict="PASS",
                   anti_patterns_observed=[], top_coaching_note="", raw="{}")


class _Run:
    def __init__(self, status, trace):
        self.status, self.trace = status, trace
        self.stderr, self.attempts = "", 1


def test_clean_pass_pipeline():
    rec = run_scenario(
        skill="audit-this-deal", scenario=_scn(), runs_idx=1, model="opus", rubric="R",
        invoke=lambda s, model: _Run("OK", _trace("Champion: Alice.", True)),
        grade=lambda **kw: _pass_verdict(),
        fetch_deal=lambda crm_id: {"status": "Open", "contacts": []},
    )
    assert rec.status == "PASS"


def test_fabrication_caught_by_scanner():
    rec = run_scenario(
        skill="audit-this-deal", scenario=_scn(), runs_idx=1, model="opus", rubric="R",
        invoke=lambda s, model: _Run("OK", _trace("Champion: Mallory Invented.", False)),
        grade=lambda **kw: _pass_verdict(),
        fetch_deal=lambda crm_id: {"status": "Open", "contacts": []},
    )
    assert rec.status == "ANTI_FAB_FAIL"


def test_stale_fixture_short_circuits():
    rec = run_scenario(
        skill="audit-this-deal",
        scenario=_scn(predicates=[{"deal_status": ["Open"]}]),
        runs_idx=1, model="opus", rubric="R",
        invoke=lambda s, model: _Run("OK", _trace("x", True)),
        grade=lambda **kw: _pass_verdict(),
        fetch_deal=lambda crm_id: {"status": "Closed won", "contacts": []},
    )
    assert rec.status == "FIXTURE_STALE"
