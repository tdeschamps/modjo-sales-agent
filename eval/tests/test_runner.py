from eval.harness.scenarios import Scenario
from eval.harness.runner import build_argv, build_prompt, invoke, RunResult


def _scn(**kw):
    base = dict(
        id="scenario-1", title="t", mode="live", prompt="/audit-deal X",
        deal_crm_id="006X", expects_shape="", predicates=[],
        synthetic_context=None, expected=[], anti=[], must_haves=[],
    )
    base.update(kw)
    return Scenario(**base)


def test_argv_is_shell_false_list_with_stream_json():
    argv = build_argv("/audit-deal X", model="opus")
    assert argv[0] == "claude"
    assert "-p" in argv
    assert "/audit-deal X" in argv
    assert "stream-json" in argv
    assert "--verbose" in argv
    assert "opus" in argv
    assert "acceptEdits" not in argv


def test_live_prompt_is_namespaced():
    # Headless plugin commands require the <plugin-name>: prefix.
    assert build_prompt(_scn()) == "/modjo-sales-agent:audit-deal X"


def test_synthetic_prompt_injects_delimited_context():
    s = _scn(mode="synthetic", deal_crm_id=None, synthetic_context="Deal Initech: EUR5000.")
    p = build_prompt(s)
    assert "/modjo-sales-agent:audit-deal X" in p
    assert "Deal Initech: EUR5000." in p
    assert "GIVEN STATE" in p


def test_invoke_uses_injected_runner_and_parses_trace():
    sample = (
        '{"type":"result","subtype":"success","is_error":false,'
        '"result":"ok","session_id":"s1","total_cost_usd":0.01,'
        '"usage":{"input_tokens":1,"output_tokens":1}}'
    )
    calls = {}

    def fake_run(argv, timeout):
        calls["argv"] = argv
        return 0, sample, ""

    rr = invoke(_scn(), model="opus", runner=fake_run)
    assert isinstance(rr, RunResult)
    assert rr.status == "OK"
    assert rr.trace.output == "ok"
    assert calls["argv"][0] == "claude"
