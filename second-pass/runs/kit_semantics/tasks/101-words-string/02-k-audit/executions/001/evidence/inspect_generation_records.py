#!/usr/bin/env python3
"""Structured, bounded inspection of all pipeline-v3 generation evidence."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path


GEN = Path("/generation-evidence")
TRACE = next((GEN / "codex-trace").rglob("*.jsonl"))


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compact(text: str, limit: int = 500) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= limit else text[:limit] + f"...<{len(text) - limit} chars omitted>"


events = []
with TRACE.open() as stream:
    for line_number, line in enumerate(stream, 1):
        events.append((line_number, json.loads(line)))

print(f"TRACE={TRACE}")
print(f"TRACE_LINES={len(events)}")
print("TOP_LEVEL_TYPES=" + repr(Counter(event["type"] for _, event in events)))
payload_types = Counter(
    event.get("payload", {}).get("type", "<none>")
    for _, event in events
)
print("PAYLOAD_TYPES=" + repr(payload_types))

session_ids = {
    event["payload"].get("session_id")
    for _, event in events
    if event["type"] == "session_meta"
}
print(f"SESSION_IDS={sorted(item for item in session_ids if item)}")

calls: dict[str, tuple[int, str]] = {}
print("TOOL_CALLS_BEGIN")
for line_number, event in events:
    payload = event.get("payload", {})
    subtype = payload.get("type")
    if subtype == "function_call":
        name = payload.get("name", "<unknown>")
        call_id = payload.get("call_id", payload.get("id", "<none>"))
        calls[call_id] = (line_number, name)
        raw_args = payload.get("arguments", "")
        try:
            args = json.loads(raw_args)
        except Exception:
            args = raw_args
        if name == "exec_command" and isinstance(args, dict):
            detail = args.get("cmd", "")
        else:
            detail = json.dumps(args, sort_keys=True) if not isinstance(args, str) else args
        print(f"line={line_number} call_id={call_id} name={name} detail={compact(detail, 1200)!r}")
    elif subtype == "custom_tool_call":
        name = payload.get("name", "<unknown>")
        call_id = payload.get("call_id", payload.get("id", "<none>"))
        calls[call_id] = (line_number, name)
        raw = payload.get("input", "")
        touched = re.findall(r"\*\*\* (?:Add|Update|Delete) File: ([^\n]+)", raw)
        print(
            f"line={line_number} call_id={call_id} name={name} "
            f"patch_files={touched!r} patch_sha256={digest(raw.encode())}"
        )
print("TOOL_CALLS_END")

print("TOOL_OUTPUT_STATUS_BEGIN")
for line_number, event in events:
    payload = event.get("payload", {})
    if payload.get("type") != "function_call_output":
        continue
    call_id = payload.get("call_id", "<none>")
    output = str(payload.get("output", ""))
    exit_codes = re.findall(r"(?:Process exited with code|EXIT_STATUS:|exit code[:=]?)\s*(-?\d+)", output, re.I)
    markers = []
    for marker in ("#Top", "WarnStuckClaimState", "EXPECTED FAILURE", "[Error]", "timed out", "oom"):
        if marker.lower() in output.lower():
            markers.append(marker)
    print(
        f"line={line_number} call_id={call_id} source_call={calls.get(call_id)!r} "
        f"chars={len(output)} exit_codes={exit_codes!r} markers={markers!r} "
        f"sha256={digest(output.encode())}"
    )
print("TOOL_OUTPUT_STATUS_END")

print("ASSISTANT_MESSAGES_BEGIN")
for line_number, event in events:
    payload = event.get("payload", {})
    if payload.get("type") != "message" or payload.get("role") != "assistant":
        continue
    pieces = []
    for item in payload.get("content", []):
        if isinstance(item, dict) and "text" in item:
            pieces.append(item["text"])
    print(
        f"line={line_number} phase={payload.get('phase')} "
        f"text={compact(chr(10).join(pieces), 2000)!r}"
    )
print("ASSISTANT_MESSAGES_END")

for name in (
    "prompt.txt",
    "codex-last.txt",
    "codex-output.log",
    "invocation.json",
    "metrics.json",
    "runtime-metrics.json",
    "usage.json",
):
    path = GEN / name
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    print(
        f"RECORD name={name} bytes={len(raw)} lines={len(text.splitlines())} "
        f"sha256={digest(raw)} utf8=YES"
    )
    if name == "codex-output.log":
        for marker in (
            "#Top",
            "WarnStuckClaimState",
            "[Error]",
            "EXPECTED FAILURE",
            "RESULT: KPROVE_PASSED",
        ):
            print(f"OUTPUT_LOG_COUNT marker={marker!r} count={text.count(marker)}")
        print(f"OUTPUT_LOG_FIRST={compact(text[:2000], 700)!r}")
        print(f"OUTPUT_LOG_LAST={compact(text[-3000:], 1000)!r}")
    elif name in {"prompt.txt", "codex-last.txt"}:
        print(f"RECORD_TEXT name={name} text={compact(text, 2500)!r}")

print("GENERATION_RECORD_INSPECTION_COMPLETE")
