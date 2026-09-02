#!/usr/bin/env python3
"""Parse every structured generation-trace record and summarize its claims."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def main() -> None:
    files = sorted(path for path in TRACE_ROOT.rglob("*") if path.is_file())
    assert files, "structured trace is empty"
    grand = 0
    for path in files:
        top_types: Counter[str] = Counter()
        payload_types: Counter[str] = Counter()
        calls: list[tuple[int, str, str, str]] = []
        final_messages: list[tuple[int, str]] = []
        lines = path.read_text().splitlines()
        for line_number, line in enumerate(lines, 1):
            obj = json.loads(line)
            assert isinstance(obj, dict)
            grand += 1
            top_types[str(obj.get("type", "<none>"))] += 1
            payload = obj.get("payload")
            if not isinstance(payload, dict):
                continue
            kind = str(payload.get("type", "<none>"))
            payload_types[kind] += 1
            if kind in {"function_call", "custom_tool_call"}:
                name = str(payload.get("name", ""))
                arguments = str(
                    payload.get("arguments", payload.get("input", ""))
                )
                calls.append(
                    (line_number, name, digest(arguments), arguments[:240])
                )
            if kind == "agent_message" and payload.get("phase") == "final_answer":
                final_messages.append((line_number, str(payload.get("message", ""))))
        print(f"file={path.relative_to(TRACE_ROOT)} lines={len(lines)}")
        print("top_types=", dict(sorted(top_types.items())))
        print("payload_types=", dict(sorted(payload_types.items())))
        print(f"tool_calls={len(calls)}")
        for line_number, name, arguments_hash, prefix in calls:
            print(
                f"  line={line_number} name={name} "
                f"arguments_sha256={arguments_hash} prefix={prefix!r}"
            )
        print(f"final_messages={len(final_messages)}")
        for line_number, message in final_messages:
            print(
                f"  line={line_number} message_sha256={digest(message)} "
                f"message={message!r}"
            )
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    print("usage_selected_event=", usage["selected_event"])
    print("parsed_structured_records=", grand)
    print("STRUCTURED_TRACE_PARSE: PASS")


if __name__ == "__main__":
    main()
