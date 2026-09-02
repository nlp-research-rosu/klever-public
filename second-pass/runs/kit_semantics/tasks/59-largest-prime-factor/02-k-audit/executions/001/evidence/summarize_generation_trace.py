#!/usr/bin/env python3
"""Bounded structural inspection of every event in the mounted JSONL trace."""

import collections
import hashlib
import json
from pathlib import Path


def main() -> int:
    root = Path("/generation-evidence/codex-trace")
    files = sorted(root.rglob("*.jsonl"))
    if not files:
        raise RuntimeError("no trace JSONL")
    for path in files:
        top_types = collections.Counter()
        payload_types = collections.Counter()
        roles = collections.Counter()
        tool_names = collections.Counter()
        first_timestamp = None
        last_timestamp = None
        line_count = 0
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for raw in stream:
                digest.update(raw)
                event = json.loads(raw)
                line_count += 1
                timestamp = event.get("timestamp")
                first_timestamp = first_timestamp or timestamp
                last_timestamp = timestamp
                top_types[event.get("type")] += 1
                payload = event.get("payload", {})
                payload_types[payload.get("type")] += 1
                if payload.get("role"):
                    roles[payload["role"]] += 1
                if payload.get("name"):
                    tool_names[payload["name"]] += 1
        print(f"file={path.relative_to(root)}")
        print(f"sha256={digest.hexdigest()}")
        print(f"lines={line_count}")
        print(f"first_timestamp={first_timestamp}")
        print(f"last_timestamp={last_timestamp}")
        print(f"top_types={dict(sorted(top_types.items(), key=lambda x: str(x[0])))}")
        print(
            "payload_types="
            f"{dict(sorted(payload_types.items(), key=lambda x: str(x[0])))}"
        )
        print(f"message_roles={dict(sorted(roles.items()))}")
        print(f"tool_calls_by_name={dict(sorted(tool_names.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
