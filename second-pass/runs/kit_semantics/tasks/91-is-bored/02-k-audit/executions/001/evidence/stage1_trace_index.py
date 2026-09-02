#!/usr/bin/env python3
"""Validate and index every event in the untrusted pipeline-v3 generation trace."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/30/"
    "rollout-2026-07-30T08-01-04-019fb31d-3a31-7290-995c-21abd2384d5b.jsonl"
)
OUTPUT = Path("/generation-evidence/codex-output.log")

top_counts = Counter()
payload_counts = Counter()
calls = []
assistant_messages = []
output_markers = Counter()
invalid = []

with TRACE.open(encoding="utf-8") as stream:
    for line_number, raw in enumerate(stream, 1):
        try:
            event = json.loads(raw)
        except Exception as error:
            invalid.append((line_number, type(error).__name__, str(error)))
            continue
        top_counts[event.get("type", "<missing>")] += 1
        payload = event.get("payload")
        if not isinstance(payload, dict):
            continue
        payload_type = payload.get("type", "<missing>")
        payload_counts[payload_type] += 1
        if payload_type in {"function_call", "custom_tool_call"}:
            name = payload.get("name", "<missing>")
            if payload_type == "function_call":
                argument_text = payload.get("arguments", "")
                try:
                    arguments = json.loads(argument_text)
                except Exception:
                    arguments = {"raw": argument_text}
                detail = arguments.get("cmd") if isinstance(arguments, dict) else None
                if detail is None:
                    detail = json.dumps(arguments, sort_keys=True)
            else:
                patch = payload.get("input", "")
                files = re.findall(r"^\*\*\* (?:Add|Update|Delete) File: (.+)$", patch, re.M)
                detail = "files=" + ",".join(files)
            calls.append((line_number, name, detail))
        if payload_type == "function_call_output":
            output = str(payload.get("output", ""))
            for marker in (
                "#Top",
                "WarnStuckClaimState",
                "[Error]",
                "Process exited with code 0",
                "Process exited with code 1",
                "Process exited with code 113",
            ):
                output_markers[marker] += output.count(marker)
        if payload_type == "message" and payload.get("role") == "assistant":
            texts = []
            for part in payload.get("content", []):
                if isinstance(part, dict) and "text" in part:
                    texts.append(str(part["text"]))
            if texts:
                assistant_messages.append(
                    (line_number, payload.get("phase", "<none>"), "\n".join(texts))
                )

raw_output = OUTPUT.read_text(encoding="utf-8", errors="replace")

print("COMMAND: python3 /audit-output/evidence/stage1_trace_index.py")
print(f"TRACE={TRACE}")
print(f"TRACE_LINES={sum(top_counts.values()) + len(invalid)}")
print(f"INVALID_JSON_LINES={len(invalid)}")
print(f"TOP_LEVEL_TYPES={dict(sorted(top_counts.items()))}")
print(f"PAYLOAD_TYPES={dict(sorted(payload_counts.items()))}")
print(f"FUNCTION_OR_PATCH_CALLS={len(calls)}")
print(f"FUNCTION_OUTPUT_MARKERS={dict(sorted(output_markers.items()))}")
print(f"CODEX_OUTPUT_LINES={len(raw_output.splitlines())}")
for marker in (
    "#Top",
    "WarnStuckClaimState",
    "RESULT: KPROVE_PASSED",
    "VALIDATED",
    "[Error]",
):
    print(f"CODEX_OUTPUT_COUNT {marker!r}={raw_output.count(marker)}")

print("CALL_INDEX:")
for line_number, name, detail in calls:
    compact = " ".join(str(detail).split())
    if len(compact) > 600:
        compact = compact[:597] + "..."
    print(f"  line={line_number} name={name} detail={compact}")

print("ASSISTANT_MESSAGE_INDEX:")
for line_number, phase, message in assistant_messages:
    compact = " ".join(message.split())
    if len(compact) > 800:
        compact = compact[:797] + "..."
    print(f"  line={line_number} phase={phase} text={compact}")

if invalid:
    print("INVALID_LINES:")
    for item in invalid:
        print(f"  {item}")
    raise SystemExit(1)

print("RESULT=PARSED_ALL_EVENTS")
