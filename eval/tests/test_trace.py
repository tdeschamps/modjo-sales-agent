from pathlib import Path
from eval.harness.trace import parse_stream, Trace, ToolCall

FIXTURE = Path(__file__).parent / "fixtures" / "sample-stream.jsonl"


def test_parses_final_output():
    t = parse_stream(FIXTURE.read_text())
    assert isinstance(t, Trace)
    assert "Champion scored 0" in t.output
    assert t.is_error is False
    assert t.session_id == "sess-abc"
    assert t.cost_usd == 0.12


def test_captures_tool_calls_with_results():
    t = parse_stream(FIXTURE.read_text())
    names = [c.name for c in t.tool_calls]
    assert "mcp__modjo__get_deals" in names
    modjo = next(c for c in t.tool_calls if c.name == "mcp__modjo__get_deals")
    assert "Planity France" in modjo.result_text
    assert "contacts" in modjo.result_text


def test_modjo_returns_helper():
    t = parse_stream(FIXTURE.read_text())
    blob = t.modjo_returns_text()
    assert "Planity France" in blob
    assert "ToolSearch" not in blob
