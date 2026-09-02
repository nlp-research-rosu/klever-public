#!/usr/bin/env python3
"""Parse every pipeline-v3 generation record and summarize untrusted claims."""

from __future__ import annotations

import collections
import json
import pathlib


JSON_RECORDS = [
    pathlib.Path("/run.json"),
    pathlib.Path("/task.json"),
    pathlib.Path("/generation-result.json"),
    pathlib.Path("/generation-evidence/invocation.json"),
    pathlib.Path("/generation-evidence/metrics.json"),
    pathlib.Path("/generation-evidence/runtime-metrics.json"),
    pathlib.Path("/generation-evidence/usage.json"),
]


def main() -> int:
    print("JSON RECORDS")
    for path in JSON_RECORDS:
        data = json.loads(path.read_text(encoding="utf-8"))
        print(f"{path}: valid JSON; top-level keys={sorted(data)}")

    trace_paths = sorted(pathlib.Path("/generation-evidence/codex-trace").rglob("*"))
    trace_files = [path for path in trace_paths if path.is_file()]
    print("\nSTRUCTURED TRACE")
    print(f"files={len(trace_files)}")
    for path in trace_files:
        outer_types: collections.Counter[str] = collections.Counter()
        payload_types: collections.Counter[str] = collections.Counter()
        first_timestamp = None
        last_timestamp = None
        line_count = 0
        for line_count, line in enumerate(path.open(encoding="utf-8"), 1):
            obj = json.loads(line)
            first_timestamp = first_timestamp or obj.get("timestamp")
            last_timestamp = obj.get("timestamp")
            outer_types[obj.get("type", "<none>")] += 1
            payload = obj.get("payload")
            if isinstance(payload, dict):
                payload_types[payload.get("type", "<none>")] += 1
        print(f"{path}: JSONL lines={line_count}")
        print(f"  first_timestamp={first_timestamp}; last_timestamp={last_timestamp}")
        print(f"  outer_types={dict(outer_types)}")
        print(f"  payload_types={dict(payload_types)}")

    print("\nTEXT RECORDS")
    for path in [
        pathlib.Path("/generation-evidence/prompt.txt"),
        pathlib.Path("/generation-evidence/codex-last.txt"),
        pathlib.Path("/generation-evidence/codex-output.log"),
    ]:
        text = path.read_text(encoding="utf-8")
        print(
            f"{path}: chars={len(text)} lines={len(text.splitlines())} "
            f"contains_NUL={chr(0) in text}"
        )
        print(f"  final_nonempty_line={next((line for line in reversed(text.splitlines()) if line), '')}")

    output = pathlib.Path("/generation-evidence/codex-output.log").read_text(encoding="utf-8")
    print("\nUNTRUSTED OUTPUT CLAIM COUNTS")
    for marker in [
        "kompile ",
        "kprove ",
        "#Top",
        "WarnStuckClaimState",
        "[Error]",
        "VALIDATED",
        "RESULT: KPROVE_PASSED",
    ]:
        print(f"{marker!r}: {output.count(marker)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
