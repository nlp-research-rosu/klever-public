#!/usr/bin/env python3
"""Read every structured trace record and summarize auditable event content."""

from __future__ import annotations

import collections
import json
from pathlib import Path


def main() -> int:
    root = Path("/generation-evidence/codex-trace")
    paths = sorted(root.rglob("*.jsonl"))
    malformed: list[tuple[str, int, str]] = []
    outer: collections.Counter[str | None] = collections.Counter()
    payloads: collections.Counter[str | None] = collections.Counter()
    function_calls: list[tuple[int, str, str]] = []
    messages: list[tuple[int, str, str]] = []

    for path in paths:
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                try:
                    record = json.loads(line)
                except Exception as error:
                    malformed.append((str(path), line_number, str(error)))
                    continue
                outer[record.get("type")] += 1
                payload = record.get("payload")
                if not isinstance(payload, dict):
                    continue
                payloads[payload.get("type")] += 1
                payload_type = payload.get("type")
                if payload_type in {"function_call", "custom_tool_call"}:
                    name = str(payload.get("name"))
                    content = payload.get("arguments", payload.get("input", ""))
                    function_calls.append((line_number, name, str(content)))
                elif payload_type in {"message", "agent_message"}:
                    content = payload.get("message", payload.get("content", ""))
                    messages.append((line_number, str(payload_type), str(content)))

    print(f"trace_files={len(paths)}")
    print(f"outer_counts={sorted(outer.items(), key=lambda item: str(item[0]))}")
    print(f"payload_counts={sorted(payloads.items(), key=lambda item: str(item[0]))}")
    print(f"malformed={malformed}")
    print("FUNCTION_CALLS")
    for line_number, name, content in function_calls:
        clipped = content if len(content) <= 4000 else content[:4000] + "...[CLIPPED]"
        print(f"line={line_number} name={name} content={clipped}")
    print("MESSAGES")
    for line_number, kind, content in messages:
        clipped = content if len(content) <= 4000 else content[:4000] + "...[CLIPPED]"
        print(f"line={line_number} kind={kind} content={clipped}")
    return 1 if malformed else 0


if __name__ == "__main__":
    raise SystemExit(main())
