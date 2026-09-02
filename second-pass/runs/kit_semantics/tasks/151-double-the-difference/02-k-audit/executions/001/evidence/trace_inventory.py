#!/usr/bin/env python3
"""Parse every structured generation-trace record and emit a bounded inventory."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sys


def main() -> int:
    traces = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    if not traces:
        print("ERROR: no structured trace")
        return 1

    for trace in traces:
        counts: Counter[str] = Counter()
        calls: dict[str, tuple[str, str]] = {}
        call_number = 0
        parsed = 0
        print(f"TRACE {trace}")
        with trace.open() as stream:
            for line_number, line in enumerate(stream, 1):
                item = json.loads(line)
                parsed += 1
                payload = item.get("payload")
                payload_type = payload.get("type", "<none>") if isinstance(payload, dict) else "<none>"
                counts[payload_type] += 1
                if payload_type in ("function_call", "custom_tool_call"):
                    call_number += 1
                    call_id = payload.get("call_id", "")
                    name = payload.get("name", "")
                    argument = payload.get("arguments", payload.get("input", ""))
                    calls[call_id] = (name, argument)
                    compact = " ".join(str(argument).split())
                    print(f"CALL {call_number} line={line_number} name={name} args={compact[:1000]}")
                elif payload_type in ("function_call_output", "custom_tool_call_output"):
                    call_id = payload.get("call_id", "")
                    output = payload.get("output", "")
                    compact = " ".join(str(output).split())
                    name = calls.get(call_id, ("<unknown>", ""))[0]
                    print(f"OUTPUT line={line_number} name={name} preview={compact[:500]}")
                elif payload_type == "agent_message":
                    compact = " ".join(payload.get("message", "").split())
                    print(
                        f"AGENT line={line_number} phase={payload.get('phase')} "
                        f"message={compact[:1000]}"
                    )
        print(f"parsed_records={parsed}")
        print(f"payload_counts={dict(sorted(counts.items()))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
