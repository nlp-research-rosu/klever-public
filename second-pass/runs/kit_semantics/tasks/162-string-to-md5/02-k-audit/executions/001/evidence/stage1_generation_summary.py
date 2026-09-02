#!/usr/bin/env python3
"""Parse every generation trace record and summarize the untrusted generation log."""

from __future__ import annotations

import collections
import glob
import hashlib
import json
from pathlib import Path


trace_paths = sorted(glob.glob("/generation-evidence/codex-trace/**/*.jsonl", recursive=True))
if not trace_paths:
    raise SystemExit("no trace JSONL found")

outer_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
roles: collections.Counter[str] = collections.Counter()
calls: dict[str, tuple[int, str, str]] = {}
outputs: dict[str, tuple[int, int, str]] = {}
parse_errors: list[tuple[str, int, str]] = []
total_lines = 0

for trace_path in trace_paths:
    with open(trace_path, encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            total_lines += 1
            try:
                record = json.loads(line)
            except Exception as error:
                parse_errors.append((trace_path, line_number, repr(error)))
                continue
            outer_types[str(record.get("type"))] += 1
            payload = record.get("payload", {})
            payload_type = str(payload.get("type"))
            payload_types[payload_type] += 1
            if payload.get("role"):
                roles[str(payload["role"])] += 1
            if payload_type in {"function_call", "custom_tool_call"}:
                argument = payload.get("arguments", payload.get("input", ""))
                calls[str(payload.get("call_id"))] = (
                    line_number,
                    str(payload.get("name")),
                    str(argument),
                )
            elif payload_type in {"function_call_output", "custom_tool_call_output"}:
                output = str(payload.get("output", ""))
                outputs[str(payload.get("call_id"))] = (
                    line_number,
                    len(output),
                    output,
                )

print("COMMAND: python3 /audit-output/evidence/stage1_generation_summary.py")
print(f"TRACE_FILES={len(trace_paths)}")
print(f"TRACE_LINES={total_lines}")
print(f"TRACE_PARSE_ERRORS={len(parse_errors)}")
print("OUTER_TYPES=" + json.dumps(outer_types, sort_keys=True))
print("PAYLOAD_TYPES=" + json.dumps(payload_types, sort_keys=True))
print("MESSAGE_ROLES=" + json.dumps(roles, sort_keys=True))
print(f"TOOL_CALLS={len(calls)}")
print(f"TOOL_OUTPUTS={len(outputs)}")
print()
print("== Complete tool-call inventory from structured trace ==")
for call_id, (line_number, name, argument) in calls.items():
    output_line, output_length, output = outputs.get(call_id, (-1, -1, ""))
    flattened = argument.replace("\r", "").replace("\n", "\\n")
    clues = []
    for marker in (
        "#Top",
        "WarnStuckClaimState",
        "VACUITY_EXIT=",
        "BODY_MUTATION_EXIT=",
        "DIFFERENTIAL_CASES=",
        "HASKELL_KRUN_EXIT=",
    ):
        if marker in output:
            clues.append(marker)
    print(
        f"TRACE_LINE={line_number} NAME={name} CALL_ID={call_id} "
        f"OUTPUT_LINE={output_line} OUTPUT_CHARS={output_length} "
        f"OUTPUT_CLUES={','.join(clues) or '-'}"
    )
    print("  ARGUMENT=" + flattened)

print()
print("== Raw generation output complete-file scan ==")
raw_path = Path("/generation-evidence/codex-output.log")
raw_bytes = raw_path.read_bytes()
raw_text = raw_bytes.decode("utf-8", errors="replace")
print(f"RAW_BYTES={len(raw_bytes)}")
print(f"RAW_LINES={len(raw_text.splitlines())}")
print(f"RAW_SHA256={hashlib.sha256(raw_bytes).hexdigest()}")
for marker in (
    "#Top",
    "WarnStuckClaimState",
    "EXPECTED_VACUITY_FAILURE",
    "EXPECTED_BODY_MUTATION_FAILURE",
    "DIFFERENTIAL_CASES=",
    "RESULT: KPROVE_PASSED",
):
    positions = [
        line_number
        for line_number, line in enumerate(raw_text.splitlines(), 1)
        if marker in line
    ]
    print(f"RAW_MARKER {marker!r} COUNT={len(positions)} LINES={positions}")

if parse_errors:
    print("PARSE_ERRORS=" + repr(parse_errors))
    raise SystemExit(1)
