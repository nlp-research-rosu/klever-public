#!/usr/bin/env python3
"""Parse every structured generation-trace record and summarize its claims."""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path


ROOT = Path("/generation-evidence/codex-trace")


def main() -> int:
    files = sorted(path for path in ROOT.rglob("*") if path.is_file())
    counts: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    commands: list[str] = []
    messages: list[str] = []
    parse_errors = 0
    total = 0
    for path in files:
        with path.open("r", encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                total += 1
                try:
                    record = json.loads(line)
                except Exception as err:
                    parse_errors += 1
                    print(f"PARSE_ERROR {path}:{line_number}: {err}")
                    continue
                kind = str(record.get("type"))
                counts[kind] += 1
                payload = record.get("payload")
                if isinstance(payload, dict):
                    payload_types[str(payload.get("type"))] += 1
                    if payload.get("type") in {"function_call", "custom_tool_call"}:
                        name = str(payload.get("name", ""))
                        arguments = str(payload.get("arguments", payload.get("input", "")))
                        if any(
                            needle in arguments
                            for needle in (
                                "kompile",
                                "kprove",
                                "krun",
                                "verification.k",
                                "spec.k",
                                "solution.py",
                                "solution.mpy",
                            )
                        ):
                            commands.append(f"{name} {arguments}")
                    if payload.get("type") in {"task_complete", "agent_message"}:
                        messages.append(str(payload))
    print(f"TRACE_FILES={[str(path.relative_to(ROOT)) for path in files]}")
    print(f"TOTAL_RECORDS={total}")
    print(f"PARSE_ERRORS={parse_errors}")
    print(f"TOP_LEVEL_TYPES={dict(sorted(counts.items()))}")
    print(f"PAYLOAD_TYPES={dict(sorted(payload_types.items()))}")
    print(f"RELEVANT_TOOL_CALLS={len(commands)}")
    for index, command in enumerate(commands, 1):
        print(f"TOOL_CALL_{index}={command}")
    print(f"TERMINAL_MESSAGES={len(messages)}")
    for index, message in enumerate(messages, 1):
        print(f"TERMINAL_{index}={message}")
    return 1 if parse_errors or not files else 0


if __name__ == "__main__":
    sys.exit(main())
