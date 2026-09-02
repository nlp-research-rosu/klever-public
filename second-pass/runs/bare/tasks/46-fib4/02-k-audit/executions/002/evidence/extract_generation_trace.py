#!/usr/bin/env python3
"""Read every generation-trace event and emit the actionable construction record."""

from __future__ import annotations

import json
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")


def text_content(content: object) -> str:
    if not isinstance(content, list):
        return repr(content)
    pieces: list[str] = []
    for item in content:
        if isinstance(item, dict):
            text = item.get("text")
            if isinstance(text, str):
                pieces.append(text)
    return "\n".join(pieces)


def main() -> None:
    for trace in sorted(TRACE_ROOT.rglob("*.jsonl")):
        print(f"TRACE {trace.relative_to(TRACE_ROOT)}")
        with trace.open() as stream:
            for line_number, line in enumerate(stream, 1):
                record = json.loads(line)
                payload = record.get("payload")
                if not isinstance(payload, dict):
                    continue
                payload_type = payload.get("type")
                if payload_type == "message":
                    role = payload.get("role")
                    # The benchmark prompt was inspected separately; include
                    # assistant messages and omit repeated framework boilerplate.
                    if role == "assistant":
                        print(
                            f"\nLINE {line_number} MESSAGE role={role}\n"
                            f"{text_content(payload.get('content'))}"
                        )
                elif payload_type in {"agent_message", "task_complete"}:
                    message = payload.get("message", "")
                    print(f"\nLINE {line_number} {payload_type}\n{message}")
                elif payload_type in {"function_call", "custom_tool_call"}:
                    name = payload.get("name")
                    arguments = payload.get("arguments", payload.get("input", ""))
                    print(f"\nLINE {line_number} CALL name={name}\n{arguments}")
                elif payload_type in {"function_call_output", "custom_tool_call_output"}:
                    output = payload.get("output", "")
                    print(f"\nLINE {line_number} OUTPUT\n{output}")


if __name__ == "__main__":
    main()
