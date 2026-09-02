#!/usr/bin/env python3
"""Structural inspection of every required pipeline-v3 generation record."""

from __future__ import annotations

import collections
import json
from pathlib import Path


REQUIRED = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/runtime-metrics.json"),
    Path("/generation-evidence/usage.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]


def main() -> None:
    for path in REQUIRED:
        if not path.is_file() or path.is_symlink():
            raise SystemExit(f"missing, mistyped, or symlinked record: {path}")
        data = path.read_bytes()
        print(
            f"record path={path} bytes={len(data)} lines={data.count(bytes([10]))} "
            f"regular=true"
        )
        if path.suffix == ".json":
            parsed = json.loads(data)
            print(
                f"json_object path={path} keys={','.join(sorted(parsed.keys()))}"
            )

    output_text = Path("/generation-evidence/codex-output.log").read_text()
    last_text = Path("/generation-evidence/codex-last.txt").read_text()
    print("untrusted_output_result_markers", output_text.count("RESULT:"))
    print("untrusted_last_result_markers", last_text.count("RESULT:"))
    print("untrusted_output_top_mentions", output_text.count("#Top"))

    trace_root = Path("/generation-evidence/codex-trace")
    if not trace_root.is_dir() or trace_root.is_symlink():
        raise SystemExit("trace root missing, mistyped, or symlinked")
    trace_files = sorted(trace_root.rglob("*.jsonl"))
    print("trace_file_count", len(trace_files))
    type_counts: collections.Counter[str] = collections.Counter()
    payload_counts: collections.Counter[str] = collections.Counter()
    response_counts: collections.Counter[str] = collections.Counter()
    total_rows = 0
    for path in trace_files:
        if not path.is_file() or path.is_symlink():
            raise SystemExit(f"bad trace entry: {path}")
        rows = 0
        for line in path.read_text().splitlines():
            row = json.loads(line)
            rows += 1
            total_rows += 1
            type_counts[row.get("type", "<missing>")] += 1
            payload = row.get("payload", {})
            if isinstance(payload, dict):
                payload_counts[payload.get("type", "<missing>")] += 1
                if row.get("type") == "response_item":
                    response_counts[payload.get("type", "<missing>")] += 1
        print(
            f"trace path={path.relative_to(trace_root)} rows={rows} "
            f"bytes={path.stat().st_size}"
        )
    print("trace_total_rows", total_rows)
    print("trace_top_types", dict(sorted(type_counts.items())))
    print("trace_payload_types", dict(sorted(payload_counts.items())))
    print("trace_response_types", dict(sorted(response_counts.items())))


if __name__ == "__main__":
    main()
