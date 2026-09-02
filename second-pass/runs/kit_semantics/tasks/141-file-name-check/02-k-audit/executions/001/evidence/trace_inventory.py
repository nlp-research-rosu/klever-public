#!/usr/bin/env python3
"""Inventory the untrusted pipeline-v3 JSONL trace without executing it."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")


def main() -> None:
    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    roles: collections.Counter[str] = collections.Counter()
    tool_names: collections.Counter[str] = collections.Counter()
    phases: collections.Counter[str] = collections.Counter()
    first_timestamp = None
    last_timestamp = None
    line_count = 0
    malformed = 0
    for path in sorted(TRACE_ROOT.rglob("*.jsonl")):
        for line in path.read_text().splitlines():
            line_count += 1
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                malformed += 1
                continue
            timestamp = record.get("timestamp")
            first_timestamp = first_timestamp or timestamp
            last_timestamp = timestamp
            top_types[str(record.get("type"))] += 1
            payload = record.get("payload")
            if not isinstance(payload, dict):
                continue
            payload_types[str(payload.get("type"))] += 1
            if "role" in payload:
                roles[str(payload["role"])] += 1
            if "name" in payload and payload.get("type") in {
                "custom_tool_call",
                "function_call",
            }:
                tool_names[str(payload["name"])] += 1
            if "phase" in payload:
                phases[str(payload["phase"])] += 1

    print(f"trace_files={len(list(TRACE_ROOT.rglob('*.jsonl')))}")
    print(f"trace_lines={line_count}")
    print(f"malformed_json_lines={malformed}")
    print(f"first_timestamp={first_timestamp}")
    print(f"last_timestamp={last_timestamp}")
    print("top_level_types=" + json.dumps(top_types, sort_keys=True))
    print("payload_types=" + json.dumps(payload_types, sort_keys=True))
    print("roles=" + json.dumps(roles, sort_keys=True))
    print("tool_names=" + json.dumps(tool_names, sort_keys=True))
    print("phases=" + json.dumps(phases, sort_keys=True))


if __name__ == "__main__":
    main()
