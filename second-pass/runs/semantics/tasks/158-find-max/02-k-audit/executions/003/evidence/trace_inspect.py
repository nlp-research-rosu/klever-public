#!/usr/bin/env python3
"""Summarize every actionable item in the untrusted generation trace."""

from __future__ import annotations

import json
from pathlib import Path


TRACE = next(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))


def clipped(value: object, limit: int = 1800) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    text = text.replace("\x00", "<NUL>")
    if len(text) <= limit:
        return text
    return text[:limit] + f"\n... <clipped {len(text) - limit} chars>"


def main() -> None:
    print("COMMAND: python3 /audit-output/evidence/trace_inspect.py")
    print(f"TRACE: {TRACE}")
    for number, line in enumerate(TRACE.open(encoding="utf-8"), start=1):
        record = json.loads(line)
        payload = record.get("payload", {})
        if not isinstance(payload, dict):
            continue
        kind = payload.get("type")
        if kind == "function_call":
            print(f"\nLINE {number} FUNCTION {payload.get('name')}")
            print(clipped(payload.get("arguments", "")))
        elif kind == "custom_tool_call":
            print(f"\nLINE {number} CUSTOM_TOOL {payload.get('name')}")
            print(clipped(payload.get("input", "")))
        elif kind in {"agent_message", "message", "task_complete"}:
            role = payload.get("role", "")
            if kind == "message" and role not in {"assistant", "user"}:
                continue
            print(f"\nLINE {number} {kind.upper()} role={role}")
            print(clipped(payload.get("message", payload.get("content", payload))))


if __name__ == "__main__":
    main()
