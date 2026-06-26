"""Parse `claude -p --output-format stream-json --verbose` output into a Trace."""
from __future__ import annotations
import json
from dataclasses import dataclass, field


@dataclass
class ToolCall:
    name: str
    input: dict
    result_text: str = ""


@dataclass
class Trace:
    output: str = ""
    tool_calls: list[ToolCall] = field(default_factory=list)
    session_id: str | None = None
    cost_usd: float | None = None
    input_tokens: int = 0
    output_tokens: int = 0
    is_error: bool = True
    raw_lines: int = 0

    def modjo_returns_text(self) -> str:
        return "\n".join(
            c.result_text for c in self.tool_calls if c.name.startswith("mcp__modjo__")
        )


def _result_to_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for blk in content:
            if isinstance(blk, dict):
                parts.append(blk.get("text") or json.dumps(blk))
            else:
                parts.append(str(blk))
        return "\n".join(parts)
    return json.dumps(content)


def parse_stream(text: str) -> Trace:
    trace = Trace()
    pending: list[ToolCall] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        trace.raw_lines += 1
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        t = obj.get("type")
        if t == "result":
            trace.output = obj.get("result", trace.output)
            trace.session_id = obj.get("session_id", trace.session_id)
            trace.cost_usd = obj.get("total_cost_usd", trace.cost_usd)
            trace.is_error = bool(obj.get("is_error", False))
            usage = obj.get("usage") or {}
            trace.input_tokens = usage.get("input_tokens", 0)
            trace.output_tokens = usage.get("output_tokens", 0)
            continue
        msg = obj.get("message")
        if not isinstance(msg, dict):
            continue
        for blk in msg.get("content") or []:
            if not isinstance(blk, dict):
                continue
            bt = blk.get("type")
            if bt == "tool_use":
                tc = ToolCall(name=blk.get("name", ""), input=blk.get("input") or {})
                trace.tool_calls.append(tc)
                pending.append(tc)
            elif bt == "tool_result":
                if pending:
                    pending.pop(0).result_text = _result_to_text(blk.get("content"))
            elif bt == "text" and not trace.output:
                trace.output = blk.get("text", "")
    return trace
