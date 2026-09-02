#!/usr/bin/env python3
"""Parse every structured trace record and inventory its complete shape."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


TRACE = Path(
    "/generation/codex-trace/2026/07/24/"
    "rollout-2026-07-24T22-25-55-019f974e-d9e5-7942-a428-43fa230d7b51.jsonl"
)


def main() -> int:
    counts: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    role_counts: collections.Counter[str] = collections.Counter()
    tool_names: collections.Counter[str] = collections.Counter()
    byte_count = 0
    parsed = 0
    first_ts = None
    last_ts = None
    malformed: list[str] = []
    sha = hashlib.sha256()
    with TRACE.open("rb") as stream:
        for line_no, raw in enumerate(stream, 1):
            sha.update(raw)
            byte_count += len(raw)
            try:
                record = json.loads(raw)
            except Exception as error:  # noqa: BLE001 - audit records exact failure
                malformed.append(f"line={line_no} error={error}")
                continue
            parsed += 1
            record_type = str(record.get("type", "<missing>"))
            counts[record_type] += 1
            timestamp = record.get("timestamp")
            if first_ts is None:
                first_ts = timestamp
            last_ts = timestamp
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_type = str(payload.get("type", "<missing>"))
                payload_types[payload_type] += 1
                role = payload.get("role")
                if role is not None:
                    role_counts[str(role)] += 1
                name = payload.get("name")
                if name is not None:
                    tool_names[str(name)] += 1
            else:
                payload_types[type(payload).__name__] += 1

    print(f"path={TRACE}")
    print(f"sha256={sha.hexdigest()}")
    print(f"bytes={byte_count}")
    print(f"parsed_lines={parsed}")
    print(f"malformed_lines={len(malformed)}")
    print(f"first_timestamp={first_ts}")
    print(f"last_timestamp={last_ts}")
    print("top_level_types=" + json.dumps(counts, sort_keys=True))
    print("payload_types=" + json.dumps(payload_types, sort_keys=True))
    print("roles=" + json.dumps(role_counts, sort_keys=True))
    print("tool_names=" + json.dumps(tool_names, sort_keys=True))
    for item in malformed:
        print(f"MALFORMED {item}")
    return 1 if malformed else 0


if __name__ == "__main__":
    raise SystemExit(main())
