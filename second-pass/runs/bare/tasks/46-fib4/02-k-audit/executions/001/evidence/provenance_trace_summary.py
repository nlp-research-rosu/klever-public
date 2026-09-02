#!/usr/bin/env python3
"""Bounded structural summary of the untrusted generation JSONL trace."""

from __future__ import annotations

import collections
import glob
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    paths = [Path(p) for p in glob.glob("/candidate/codex-trace/**/*.jsonl", recursive=True)]
    reports = []
    invalid_total = 0
    for path in sorted(paths):
        top_types: collections.Counter[str] = collections.Counter()
        event_types: collections.Counter[str] = collections.Counter()
        response_types: collections.Counter[str] = collections.Counter()
        function_calls: collections.Counter[str] = collections.Counter()
        invalid = []
        line_count = 0
        with path.open(encoding="utf-8") as stream:
            for lineno, line in enumerate(stream, 1):
                line_count += 1
                try:
                    obj = json.loads(line)
                except Exception as err:
                    invalid.append({"line": lineno, "error": str(err)})
                    continue
                top_type = obj.get("type", "<missing>") if isinstance(obj, dict) else "<nonobject>"
                top_types[top_type] += 1
                payload = obj.get("payload", {}) if isinstance(obj, dict) else {}
                if top_type == "event_msg" and isinstance(payload, dict):
                    event_types[payload.get("type", "<missing>")] += 1
                if top_type == "response_item" and isinstance(payload, dict):
                    response_type = payload.get("type", "<missing>")
                    response_types[response_type] += 1
                    if response_type == "function_call":
                        function_calls[payload.get("name", "<missing>")] += 1
        invalid_total += len(invalid)
        reports.append(
            {
                "path": str(path),
                "sha256": sha256(path),
                "line_count": line_count,
                "regular_file": path.is_file() and not path.is_symlink(),
                "invalid_json_lines": invalid,
                "top_level_types": dict(sorted(top_types.items())),
                "event_payload_types": dict(sorted(event_types.items())),
                "response_item_types": dict(sorted(response_types.items())),
                "function_calls": dict(sorted(function_calls.items())),
            }
        )
    print(json.dumps({"trace_count": len(paths), "traces": reports}, indent=2, sort_keys=True))
    return 1 if invalid_total or not paths else 0


if __name__ == "__main__":
    raise SystemExit(main())
