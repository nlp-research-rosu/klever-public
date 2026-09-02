#!/usr/bin/env python3
"""Bounded structural inspection of the complete untrusted generation records."""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path


trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
trace_files = [path for path in trace_files if path.is_file()]
print(f"trace_files={len(trace_files)}")

outer_types = collections.Counter()
payload_types = collections.Counter()
function_names = collections.Counter()
trace_lines = 0
malformed = []
first_timestamp = None
last_timestamp = None
final_messages = []

for path in trace_files:
    print(f"trace_file={path} bytes={path.stat().st_size}")
    with path.open() as stream:
        for line_number, line in enumerate(stream, 1):
            trace_lines += 1
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                malformed.append((str(path), line_number, str(error)))
                continue
            timestamp = record.get("timestamp")
            first_timestamp = first_timestamp or timestamp
            last_timestamp = timestamp
            outer_types[record.get("type", "<missing>")] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_type = payload.get("type", "<missing>")
                payload_types[payload_type] += 1
                name = payload.get("name")
                if isinstance(name, str):
                    function_names[name] += 1
                if (
                    payload_type == "message"
                    and payload.get("role") == "assistant"
                    and payload.get("phase") == "final_answer"
                ):
                    final_messages.append(payload.get("content"))

print(f"trace_lines={trace_lines} malformed_json_lines={len(malformed)}")
print(f"first_timestamp={first_timestamp} last_timestamp={last_timestamp}")
print(f"outer_types={dict(sorted(outer_types.items()))}")
print(f"payload_types={dict(sorted(payload_types.items()))}")
print(f"function_names={dict(sorted(function_names.items()))}")
print(f"final_messages={len(final_messages)}")
for error in malformed[:20]:
    print(f"malformed={error!r}")

output_path = Path("/generation-evidence/codex-output.log")
output = output_path.read_text(errors="replace")
output_lines = output.splitlines()
patterns = {
    "exact_top": r"(?m)^#Top$",
    "warn_stuck": r"WarnStuckClaimState",
    "kprove": r"\bkprove\b",
    "kompile": r"\bkompile\b",
    "result_passed": r"RESULT: KPROVE_PASSED",
    "verification_mentions": r"verification\.k",
    "spec_mentions": r"spec\.k",
}
print(f"codex_output_bytes={output_path.stat().st_size} lines={len(output_lines)}")
for label, pattern in patterns.items():
    print(f"codex_output_count.{label}={len(re.findall(pattern, output))}")

print("codex_output_first_12_lines:")
for line in output_lines[:12]:
    print(f"  {line[:300]}")
print("codex_output_last_12_lines:")
for line in output_lines[-12:]:
    print(f"  {line[:300]}")

if malformed:
    raise SystemExit(1)
