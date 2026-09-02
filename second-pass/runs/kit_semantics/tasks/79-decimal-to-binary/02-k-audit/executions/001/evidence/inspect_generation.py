#!/usr/bin/env python3
"""Read and summarize every required pipeline-v3 generation record."""

from __future__ import annotations

import collections
import json
from pathlib import Path


JSON_RECORDS = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/runtime-metrics.json"),
    Path("/generation-evidence/usage.json"),
]
TEXT_RECORDS = [
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]


def main() -> None:
    for path in JSON_RECORDS:
        document = json.loads(path.read_text(encoding="utf-8"))
        print(
            f"JSON_OK path={path} bytes={path.stat().st_size} "
            f"keys={sorted(document)}"
        )

    for path in TEXT_RECORDS:
        text = path.read_text(encoding="utf-8")
        print(
            f"TEXT_READ path={path} bytes={len(text.encode())} "
            f"lines={len(text.splitlines())}"
        )
        if path.name != "codex-output.log":
            print(f"BEGIN_{path.name}")
            print(text.rstrip())
            print(f"END_{path.name}")

    output = Path("/generation-evidence/codex-output.log").read_text()
    print(
        "CODEX_OUTPUT_MARKERS "
        f"top_lines={sum(line == '#Top' for line in output.splitlines())} "
        f"result_markers={sum('RESULT:' in line for line in output.splitlines())} "
        f"expected_failure_mentions={output.count('EXPECTED FAILURE')}"
    )

    trace_files = sorted(
        Path("/generation-evidence/codex-trace").rglob("*.jsonl")
    )
    print(f"TRACE_FILES={len(trace_files)}")
    overall_types: collections.Counter[str] = collections.Counter()
    overall_payload_types: collections.Counter[str] = collections.Counter()
    commands = []
    bad_json = []
    total_lines = 0
    for path in trace_files:
        first_timestamp = None
        last_timestamp = None
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                total_lines += 1
                try:
                    record = json.loads(line)
                except Exception as error:
                    bad_json.append((str(path), line_number, repr(error)))
                    continue
                if first_timestamp is None:
                    first_timestamp = record.get("timestamp")
                last_timestamp = record.get("timestamp")
                overall_types[record.get("type", "<none>")] += 1
                payload = record.get("payload", {})
                if isinstance(payload, dict):
                    payload_type = payload.get("type", "<none>")
                    overall_payload_types[payload_type] += 1
                    if payload_type in ("function_call", "custom_tool_call"):
                        commands.append(
                            (
                                line_number,
                                payload.get("name"),
                                str(payload.get("arguments", ""))[:300],
                            )
                        )
        print(
            f"TRACE_READ path={path} first={first_timestamp} "
            f"last={last_timestamp}"
        )

    print(f"TRACE_LINES={total_lines} BAD_JSON={len(bad_json)}")
    print(f"TRACE_RECORD_TYPES={dict(sorted(overall_types.items()))}")
    print(f"TRACE_PAYLOAD_TYPES={dict(sorted(overall_payload_types.items()))}")
    print(f"TRACE_TOOL_CALLS={len(commands)}")
    for command in commands:
        print("TRACE_TOOL_CALL", command)
    assert not bad_json
    print("GENERATION_RECORD_INSPECTION=PASS")


if __name__ == "__main__":
    main()
