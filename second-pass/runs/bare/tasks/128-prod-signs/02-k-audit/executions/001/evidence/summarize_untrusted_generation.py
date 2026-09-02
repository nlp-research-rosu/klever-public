#!/usr/bin/env python3
"""Bounded metadata summary of candidate generation records.

The records are treated as untrusted text and are never executed.
"""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


CANDIDATE = Path("/candidate")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    paths = [
        CANDIDATE / "run-input.json",
        CANDIDATE / "metrics.json",
        CANDIDATE / "codex-last.txt",
        CANDIDATE / "codex-output.log",
    ]
    trace_paths = sorted((CANDIDATE / "codex-trace").rglob("*.jsonl"))
    paths.extend(trace_paths)

    print("FILES")
    for path in paths:
        print(f"{path} bytes={path.stat().st_size} sha256={digest(path)}")

    print("RUN_INPUT")
    run_input = json.loads((CANDIDATE / "run-input.json").read_text())
    print(json.dumps(run_input, sort_keys=True))

    print("METRICS")
    metrics = json.loads((CANDIDATE / "metrics.json").read_text())
    print(json.dumps(metrics, sort_keys=True))

    last_lines = (CANDIDATE / "codex-last.txt").read_text().splitlines()
    print(f"CODEX_LAST lines={len(last_lines)}")
    for line in last_lines:
        if "exited" in line or "kprove" in line or line.startswith("RESULT:"):
            print(f"UNTRUSTED_CLAIM {line}")

    output_lines = (CANDIDATE / "codex-output.log").read_text(
        errors="replace"
    ).splitlines()
    print(
        "CODEX_OUTPUT "
        f"lines={len(output_lines)} "
        f"top_mentions={sum('#Top' in line for line in output_lines)} "
        f"kprove_mentions={sum('kprove' in line for line in output_lines)} "
        f"krun_mentions={sum('krun' in line for line in output_lines)}"
    )
    result_markers = [line for line in output_lines if line.startswith("RESULT:")]
    for line in result_markers[-3:]:
        print(f"UNTRUSTED_RESULT_MARKER {line}")

    for trace_path in trace_paths:
        outer_types: collections.Counter[str] = collections.Counter()
        payload_types: collections.Counter[str] = collections.Counter()
        malformed = 0
        line_count = 0
        with trace_path.open() as stream:
            for raw_line in stream:
                line_count += 1
                try:
                    record = json.loads(raw_line)
                except json.JSONDecodeError:
                    malformed += 1
                    continue
                outer_types[str(record.get("type"))] += 1
                payload = record.get("payload")
                if isinstance(payload, dict) and "type" in payload:
                    payload_types[str(payload["type"])] += 1
        print(
            f"TRACE {trace_path} lines={line_count} malformed={malformed} "
            f"outer_types={dict(sorted(outer_types.items()))} "
            f"payload_types={dict(sorted(payload_types.items()))}"
        )


if __name__ == "__main__":
    main()
