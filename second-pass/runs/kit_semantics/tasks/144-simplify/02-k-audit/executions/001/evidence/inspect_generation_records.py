#!/usr/bin/env python3
"""Read every untrusted pipeline-v3 log/trace record and emit a bounded index."""

from __future__ import annotations

import collections
import glob
import json
import re
from pathlib import Path


trace_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
call_names: collections.Counter[str] = collections.Counter()
relevant_calls: list[str] = []
trace_lines = 0

for name in sorted(
    glob.glob("/generation-evidence/codex-trace/**/*.jsonl", recursive=True)
):
    with open(name, encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            trace_lines += 1
            record = json.loads(line)
            trace_types[str(record.get("type"))] += 1
            payload = record.get("payload") or {}
            payload_type = str(payload.get("type"))
            payload_types[payload_type] += 1
            if payload_type in {"function_call", "custom_tool_call"}:
                call_name = str(payload.get("name"))
                call_names[call_name] += 1
                arguments = str(payload.get("arguments", ""))
                if re.search(
                    r"\b(kompile|kprove|krun|prove\.sh|"
                    r"verification\.k|loop-spec\.k|spec\.k)\b",
                    arguments,
                ):
                    relevant_calls.append(
                        f"{Path(name).name}:{line_number}:{call_name}:"
                        f"{arguments[:500]}"
                    )

log_path = Path("/generation-evidence/codex-output.log")
log_lines = 0
marker_counts: collections.Counter[str] = collections.Counter()
patterns = {
    "#Top": re.compile(r"#Top"),
    "WarnStuckClaimState": re.compile(r"WarnStuckClaimState"),
    "timeout": re.compile(r"\btimeout\b", re.IGNORECASE),
    "kprove": re.compile(r"\bkprove\b"),
    "kompile": re.compile(r"\bkompile\b"),
    "krun": re.compile(r"\bkrun\b"),
    "RESULT_KPROVE_PASSED": re.compile(r"RESULT: KPROVE_PASSED"),
}
with log_path.open(encoding="utf-8", errors="replace") as stream:
    for line in stream:
        log_lines += 1
        for label, pattern in patterns.items():
            marker_counts[label] += len(pattern.findall(line))

print(f"trace_json_lines={trace_lines}")
print(f"trace_outer_types={dict(sorted(trace_types.items()))}")
print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
print(f"trace_call_names={dict(sorted(call_names.items()))}")
print(f"codex_output_lines={log_lines}")
print(f"codex_output_marker_counts={dict(sorted(marker_counts.items()))}")
print(f"relevant_trace_calls={len(relevant_calls)}")
for call in relevant_calls[-40:]:
    print(f"TRACE_CALL {call}")
print("NOTE: generation records are indexed as untrusted claims only")
print("EXIT_STATUS: 0")
