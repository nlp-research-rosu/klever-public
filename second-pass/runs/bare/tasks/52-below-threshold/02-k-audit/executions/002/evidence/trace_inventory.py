#!/usr/bin/env python3
"""Validate and inventory every structured generation-trace record."""

from __future__ import annotations

import collections
import json
from pathlib import Path


def main() -> int:
    root = Path("/generation-evidence/codex-trace")
    files = sorted(root.rglob("*.jsonl"))
    assert files, "no structured trace"
    outer = collections.Counter()
    payload = collections.Counter()
    roles = collections.Counter()
    commands: list[str] = []
    malformed = 0
    lines = 0

    for path in files:
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                lines += 1
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    malformed += 1
                    print(f"malformed {path}:{line_number}")
                    continue
                outer[record.get("type", "<missing>")] += 1
                body = record.get("payload")
                if isinstance(body, dict):
                    payload[body.get("type", "<missing>")] += 1
                    if isinstance(body.get("role"), str):
                        roles[body["role"]] += 1
                    if body.get("type") == "function_call":
                        args = body.get("arguments")
                        commands.append(
                            f"{body.get('name')} {args if isinstance(args, str) else json.dumps(args, sort_keys=True)}"
                        )
                    elif body.get("type") == "custom_tool_call":
                        raw_input = body.get("input")
                        commands.append(
                            f"{body.get('name')} {raw_input if isinstance(raw_input, str) else json.dumps(raw_input, sort_keys=True)}"
                        )

    print("trace files:")
    for path in files:
        print(path.relative_to(root))
    print("records:", lines)
    print("malformed records:", malformed)
    print("outer types:", dict(sorted(outer.items())))
    print("payload types:", dict(sorted(payload.items())))
    print("message roles:", dict(sorted(roles.items())))
    print("function calls:", len(commands))
    for number, command in enumerate(commands, 1):
        compact = " ".join(command.split())
        print(f"call {number}: {compact[:500]}")
    assert malformed == 0
    print("TRACE_INVENTORY: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
