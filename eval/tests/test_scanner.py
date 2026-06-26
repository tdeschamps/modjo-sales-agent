from eval.harness.trace import Trace, ToolCall
from eval.harness.scanner import scan, ScanResult


def _trace_with_returns(returns_text: str, output: str) -> Trace:
    t = Trace(output=output, is_error=False)
    t.tool_calls.append(ToolCall(name="mcp__modjo__get_deals", input={}, result_text=returns_text))
    return t


def test_flags_champion_not_in_returns():
    t = _trace_with_returns(
        '{"contacts":[{"name":"Bob Smith","role":"Decision Maker"}]}',
        "Champion: Alice Jones is the clear champion driving this deal.",
    )
    res = scan(t, forbidden_entities=[])
    assert isinstance(res, ScanResult)
    assert res.anti_fab_fail is True
    assert any("Alice Jones" in f for f in res.findings)


def test_passes_when_champion_present_in_returns():
    t = _trace_with_returns(
        '{"contacts":[{"name":"Alice Jones","role":"Champion"}]}',
        "Champion: Alice Jones (tagged Champion in CRM).",
    )
    res = scan(t, forbidden_entities=[])
    assert res.anti_fab_fail is False


def test_flags_explicit_forbidden_entity():
    t = _trace_with_returns('{"contacts":[]}', "We lost to Competitor X last quarter.")
    res = scan(t, forbidden_entities=["Competitor X"])
    assert res.anti_fab_fail is True
    assert any("Competitor X" in f for f in res.findings)


def test_synthetic_returns_empty_oracle_is_skipped():
    t = Trace(output="Champion: Alice.", is_error=False)
    res = scan(t, forbidden_entities=[])
    assert res.anti_fab_fail is False
    assert res.skipped_no_oracle is True
