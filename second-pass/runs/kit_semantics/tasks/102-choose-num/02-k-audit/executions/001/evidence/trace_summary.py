#!/usr/bin/env python3
"""Parse every JSONL record in the structured generation trace."""

from __future__ import annotations

import collections
import json
from pathlib import Path


def main() -> None:
    paths = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    assert paths
    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    function_calls: collections.Counter[str] = collections.Counter()
    malformed = 0
    total = 0
    final_messages: list[str] = []
    for path in paths:
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    malformed += 1
                    continue
                total += 1
                top_types[str(record.get("type"))] += 1
                payload = record.get("payload")
                if isinstance(payload, dict):
                    payload_types[str(payload.get("type"))] += 1
                    if payload.get("type") == "function_call":
                        function_calls[str(payload.get("name"))] += 1
                    if payload.get("type") == "agent_message" and payload.get("phase") == "final_answer":
                        final_messages.append(str(payload.get("message")))
    print(f"trace_files={len(paths)} records={total} malformed={malformed}")
    print("top_types=" + json.dumps(dict(sorted(top_types.items())), sort_keys=True))
    print("payload_types=" + json.dumps(dict(sorted(payload_types.items())), sort_keys=True))
    print("function_calls=" + json.dumps(dict(sorted(function_calls.items())), sort_keys=True))
    print(f"final_messages={len(final_messages)}")
    for index, message in enumerate(final_messages, 1):
        print(f"final_message_{index}={message!r}")
    assert malformed == 0
    assert total == 223
    print("TRACE_PARSE=PASS")


if __name__ == "__main__":
    main()
