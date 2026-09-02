#!/usr/bin/env python3
"""Bounded summary of the complete untrusted generation/provenance record."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path


def digest(path: Path) -> tuple[str, int, int, str]:
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest(), len(data), data.count(b"\n"), data.decode("utf-8")


def main() -> int:
    if len(sys.argv) != 7:
        print(
            "usage: provenance_summary.py RUN_INPUT METRICS CODEX_LAST CODEX_OUTPUT TRACE_JSONL EXPECTED_PROMPT_HASH",
            file=sys.stderr,
        )
        return 64

    run_input_path, metrics_path, last_path, output_path, trace_path = map(Path, sys.argv[1:6])
    expected_prompt_hash = sys.argv[6]
    loaded: dict[Path, str] = {}
    for path in (run_input_path, metrics_path, last_path, output_path, trace_path):
        sha, size, lines, text = digest(path)
        loaded[path] = text
        print(f"FILE {path} bytes={size} lines={lines} sha256={sha}")

    run_input = json.loads(loaded[run_input_path])
    metrics = json.loads(loaded[metrics_path])
    print("RUN_INPUT " + json.dumps(run_input, sort_keys=True))
    print("METRICS " + json.dumps(metrics, sort_keys=True))
    print(f"PROMPT_HASH_CLAIM_MATCHES_TRUSTED={run_input['inputs']['problem_prompt_sha256'] == expected_prompt_hash}")
    print("CODEX_LAST_BEGIN")
    print(loaded[last_path].rstrip())
    print("CODEX_LAST_END")

    output = loaded[output_path]
    print(f"CODEX_OUTPUT_success_markers={len(re.findall(r'^ succeeded in ', output, flags=re.MULTILINE))}")
    print(f"CODEX_OUTPUT_failure_markers={len(re.findall(r'^ failed', output, flags=re.MULTILINE))}")
    print(f"CODEX_OUTPUT_top_occurrences={output.count('#Top')}")
    print("CODEX_OUTPUT_RELEVANT_COMMANDS_BEGIN")
    command_lines = []
    for line in output.splitlines():
        if line.startswith("/bin/bash -lc ") and any(
            word in line for word in ("kompile", "krun", "kprove", "py2mpy.py", "prove.sh")
        ):
            if line not in command_lines:
                command_lines.append(line)
    for line in command_lines[:80]:
        print(line)
    print(f"unique_relevant_command_lines={len(command_lines)} printed={min(80, len(command_lines))}")
    print("CODEX_OUTPUT_RELEVANT_COMMANDS_END")

    trace_counts: Counter[tuple[str, str]] = Counter()
    call_names: Counter[str] = Counter()
    trace_records = 0
    for line_number, line in enumerate(loaded[trace_path].splitlines(), 1):
        record = json.loads(line)
        trace_records += 1
        payload = record.get("payload", {})
        trace_counts[(record.get("type", ""), payload.get("type", ""))] += 1
        if payload.get("type") == "custom_tool_call":
            call_names[payload.get("name", "")] += 1
    print(f"TRACE parsed_records={trace_records}")
    for key, count in sorted(trace_counts.items()):
        print(f"TRACE_TYPE outer={key[0]!r} inner={key[1]!r} count={count}")
    for name, count in sorted(call_names.items()):
        print(f"TRACE_TOOL name={name!r} count={count}")
    print("NOTE: all values above are untrusted provenance claims, not proof evidence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
