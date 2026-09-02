#!/usr/bin/env python3
"""Read and summarize every structured generation-trace event and output-log line."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")
OUTPUT_LOG = Path("/generation-evidence/codex-output.log")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


trace_files = sorted(TRACE_ROOT.rglob("*.jsonl"))
top_types = collections.Counter()
payload_types = collections.Counter()
calls = []
call_outputs = {}
event_count = 0
malformed = []
for trace_path in trace_files:
    with trace_path.open() as handle:
        for line_number, line in enumerate(handle, 1):
            event_count += 1
            try:
                event = json.loads(line)
            except Exception as error:
                malformed.append((str(trace_path), line_number, repr(error)))
                continue
            top_types[event.get("type")] += 1
            payload = event.get("payload")
            if not isinstance(payload, dict):
                continue
            payload_types[payload.get("type")] += 1
            if payload.get("type") in {"function_call", "custom_tool_call"}:
                raw_arguments = payload.get("arguments", payload.get("input", ""))
                if not isinstance(raw_arguments, str):
                    raw_arguments = json.dumps(raw_arguments, sort_keys=True)
                calls.append(
                    (
                        payload.get("call_id", payload.get("id", "")),
                        payload.get("name", ""),
                        raw_arguments,
                    )
                )
            elif payload.get("type") in {
                "function_call_output",
                "custom_tool_call_output",
            }:
                raw_output = payload.get("output", "")
                if not isinstance(raw_output, str):
                    raw_output = json.dumps(raw_output, sort_keys=True)
                call_outputs[payload.get("call_id", payload.get("id", ""))] = raw_output

print(f"TRACE_FILES={len(trace_files)}")
print(f"TRACE_EVENTS_READ={event_count}")
print(f"TRACE_MALFORMED_EVENTS={len(malformed)}")
print("TRACE_TOP_TYPES=", dict(sorted(top_types.items(), key=lambda item: str(item[0]))))
print(
    "TRACE_PAYLOAD_TYPES=",
    dict(sorted(payload_types.items(), key=lambda item: str(item[0]))),
)
print(f"TRACE_TOOL_CALLS={len(calls)}")
print(f"TRACE_TOOL_OUTPUTS={len(call_outputs)}")
for sequence, (call_id, name, arguments) in enumerate(calls, 1):
    output = call_outputs.get(call_id, "")
    argument_bytes = arguments.encode()
    output_bytes = output.encode()
    argument_preview = arguments.replace("\n", "\\n")[:500]
    output_preview = output.replace("\n", "\\n")[:500]
    print(
        f"CALL {sequence} id={call_id} name={name} "
        f"arg_bytes={len(argument_bytes)} arg_sha256={digest(argument_bytes)} "
        f"out_bytes={len(output_bytes)} out_sha256={digest(output_bytes)}"
    )
    print(f"  ARG_PREVIEW={argument_preview}")
    print(f"  OUT_PREVIEW={output_preview}")

output_bytes = OUTPUT_LOG.read_bytes()
output_text = output_bytes.decode("utf-8", errors="replace")
output_lines = output_text.splitlines()
markers = [
    "#Top",
    "WarnStuckClaimState",
    "kprove ",
    "kompile ",
    "verification.k",
    "spec.k",
    "simplification",
    "RESULT:",
]
print(f"CODEX_OUTPUT_BYTES_READ={len(output_bytes)}")
print(f"CODEX_OUTPUT_LINES_READ={len(output_lines)}")
print(f"CODEX_OUTPUT_SHA256={digest(output_bytes)}")
for marker in markers:
    print(f"CODEX_OUTPUT_MARKER {marker!r} COUNT={output_text.count(marker)}")
print("CODEX_OUTPUT_RELEVANT_TAIL:")
relevant = [
    f"{line_number}:{line}"
    for line_number, line in enumerate(output_lines, 1)
    if any(marker in line for marker in markers)
]
for line in relevant[-80:]:
    print(line[:1200])
