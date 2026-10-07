"""Canonical loop stream: one normalized JSONL record per event.

The runner is the sole producer of ``stream.jsonl``; a host's ``watch``/``report`` are
read-only consumers. Keeping the schema and the agent-event mapping here (imported by
both producer and consumer) prevents drift. Project-agnostic.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

STREAM_FILE = "stream.jsonl"

# Event kinds. ``supervise.*``/``step``/``coverage``/``issues`` are produced by the
# runner; ``agent.*`` are normalized from the spawned agent's JSON stdout.
SUPERVISE_START = "supervise.start"
SUPERVISE_END = "supervise.end"
SUPERVISE_REFUSED = "supervise.refused"
SUPERVISE_ERROR = "supervise.error"
SUPERVISE_STOP = "supervise.stop"
STEP = "step"
COVERAGE = "coverage"
ISSUES = "issues"
TOOL = "agent.tool"
TEXT = "agent.text"
REASONING = "agent.reasoning"
TOKENS = "agent.tokens"
RAW = "agent.raw"

# Agent tool-input keys, in preference order, used to summarize a tool call.
_TOOL_INPUT_KEYS = (
    "command",
    "filePath",
    "pattern",
    "path",
    "description",
    "url",
    "query",
)


def _short(text: Any, limit: int = 400) -> str:
    collapsed = " ".join(str(text).split())
    return collapsed if len(collapsed) <= limit else collapsed[: limit - 3] + "..."


def tool_summary(input_: dict[str, Any] | None) -> str:
    """Human summary of a tool call's primary argument (for display/dedup)."""
    if not isinstance(input_, dict) or not input_:
        return ""
    for key in _TOOL_INPUT_KEYS:
        value = input_.get(key)
        if value:
            return _short(value)
    return _short(json.dumps(input_, sort_keys=True))


def normalize_agent_event(line: str) -> dict[str, Any] | None:
    """Map one raw agent ``--format json`` stdout line to a stream record.

    Returns ``None`` for events that carry no watch-worthy signal (heartbeats,
    session bookkeeping), so ``stream.jsonl`` stays signal-dense.
    """
    line = line.strip()
    if not line:
        return None
    try:
        event = json.loads(line)
    except json.JSONDecodeError:
        return {"kind": RAW, "text": _short(line, 1000)}
    if not isinstance(event, dict):
        return {"kind": RAW, "text": _short(line, 1000)}

    kind = event.get("type")
    raw_part = event.get("part")
    part: dict[str, Any] = raw_part if isinstance(raw_part, dict) else {}
    session = event.get("sessionID") or part.get("sessionID")

    if kind == "tool_use":
        raw_state = part.get("state")
        state: dict[str, Any] = raw_state if isinstance(raw_state, dict) else {}
        raw_input = state.get("input")
        input_: dict[str, Any] = raw_input if isinstance(raw_input, dict) else {}
        record: dict[str, Any] = {
            "kind": TOOL,
            "tool": part.get("tool") or part.get("title") or "tool",
            "input": input_,
            "status": state.get("status"),
            "output": _short(state.get("output", ""), 2000)
            if state.get("output")
            else "",
        }
        if session:
            record["session"] = session
        return record

    if kind == "text" and part.get("text"):
        record = {"kind": TEXT, "text": str(part["text"])}
        if session:
            record["session"] = session
        return record

    if kind == "reasoning" and part.get("text"):
        return {"kind": REASONING, "text": str(part["text"])}

    if kind == "step_finish":
        raw_tokens = part.get("tokens")
        tokens: dict[str, Any] = raw_tokens if isinstance(raw_tokens, dict) else {}
        return {
            "kind": TOKENS,
            "input": int(tokens.get("input", 0) or 0),
            "output": int(tokens.get("output", 0) or 0),
            "reasoning": int(tokens.get("reasoning", 0) or 0),
            "cost": float(part.get("cost", 0.0) or 0.0),
        }

    return None


def read_stream(path: Path | str) -> list[dict[str, Any]]:
    """Parse a ``stream.jsonl`` file into records (empty if absent/unreadable)."""
    path = Path(path)
    if not path.is_file():
        return []
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(record, dict):
            records.append(record)
    return records


def render_event(record: dict[str, Any]) -> str:
    """One compact, human-readable line for a stream record (host ``watch``)."""
    kind = record.get("kind", "?")
    if kind == TOOL:
        return f"  tool      {record.get('tool', '?')}: {tool_summary(record.get('input'))}"
    if kind == TEXT:
        return f"  agent     {_short(record.get('text'), 300)}"
    if kind == REASONING:
        return f"  think     {_short(record.get('text'), 300)}"
    if kind == TOKENS:
        return (
            f"  tokens    in={record.get('input')} out={record.get('output')} "
            f"cost={record.get('cost')}"
        )
    if kind == STEP:
        entry = record.get("entry") or {}
        return f"  step {entry.get('step')} [{entry.get('axis', '?')}]"
    if kind == COVERAGE:
        return (
            f"  coverage  {record.get('verified', 0)}/{record.get('total', 0)} "
            f"complete={record.get('complete')}"
        )
    if kind == ISSUES:
        return f"  issues    complete={record.get('complete')} counts={record.get('counts')}"
    if kind in (
        SUPERVISE_START,
        SUPERVISE_END,
        SUPERVISE_REFUSED,
        SUPERVISE_ERROR,
        SUPERVISE_STOP,
    ):
        return f"  {kind:<16} {json.dumps({k: v for k, v in record.items() if k != 'kind'})[:200]}"
    return f"  {kind:<16}"


__all__ = [
    "COVERAGE",
    "ISSUES",
    "RAW",
    "REASONING",
    "STEP",
    "STREAM_FILE",
    "SUPERVISE_END",
    "SUPERVISE_ERROR",
    "SUPERVISE_REFUSED",
    "SUPERVISE_START",
    "SUPERVISE_STOP",
    "TEXT",
    "TOKENS",
    "TOOL",
    "normalize_agent_event",
    "read_stream",
    "render_event",
    "tool_summary",
]
