#!/usr/bin/env python3
"""Scan the complete untrusted generation log/trace and summarize their claims."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


LOG = Path("/candidate/codex-output.log")
TRACE = next(Path("/candidate/codex-trace").rglob("*.jsonl"))
KEYWORDS = (
    "kprove",
    "kompile",
    "krun",
    "#Top",
    "SOUND-BUT-LIMITED",
    "Gate A",
    "WarnStuckClaimState",
    "mismatches=",
    "body-mutant",
    "spec-vacuity",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


print(f"CODEX_LOG path={LOG} bytes={LOG.stat().st_size} sha256={digest(LOG)}")
log_counts: collections.Counter[str] = collections.Counter()
log_hits: list[tuple[int, str]] = []
with LOG.open("r", errors="replace") as stream:
    for line_number, line in enumerate(stream, 1):
        for keyword in KEYWORDS:
            if keyword in line:
                log_counts[keyword] += 1
                if len(log_hits) < 160:
                    log_hits.append((line_number, line.rstrip()[:500]))
print("CODEX_LOG_KEYWORD_COUNTS", dict(log_counts))
print("CODEX_LOG_FIRST_RELEVANT_LINES")
for line_number, line in log_hits:
    print(f"{line_number}: {line}")

print(f"TRACE path={TRACE} bytes={TRACE.stat().st_size} sha256={digest(TRACE)}")
top_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
calls: list[tuple[int, str, str]] = []
messages: list[tuple[int, str, str]] = []
json_errors: list[str] = []
with TRACE.open("r", errors="replace") as stream:
    for line_number, line in enumerate(stream, 1):
        try:
            event = json.loads(line)
        except Exception as error:  # pragma: no cover - audit diagnostic
            json_errors.append(f"line={line_number} error={error!r}")
            continue
        event_type = str(event.get("type"))
        top_types[event_type] += 1
        payload = event.get("payload")
        if not isinstance(payload, dict):
            continue
        payload_type = str(payload.get("type"))
        payload_types[payload_type] += 1
        if event_type == "response_item" and payload_type == "function_call":
            calls.append(
                (
                    line_number,
                    str(payload.get("name")),
                    str(payload.get("arguments"))[:1200],
                )
            )
        if event_type == "response_item" and payload_type == "message":
            role = str(payload.get("role"))
            pieces = payload.get("content", [])
            text = " ".join(
                str(piece.get("text", ""))
                for piece in pieces
                if isinstance(piece, dict)
            )
            if role in {"assistant", "user"}:
                messages.append((line_number, role, text[-1200:]))
        if event_type == "event_msg" and payload_type == "agent_message":
            messages.append(
                (line_number, "agent_message", str(payload.get("message", ""))[-1200:])
            )

print("TRACE_TOP_TYPES", dict(top_types))
print("TRACE_PAYLOAD_TYPES", dict(payload_types))
print(f"TRACE_JSON_ERRORS count={len(json_errors)} details={json_errors}")
print(f"TRACE_FUNCTION_CALL_COUNT {len(calls)}")
for line_number, name, arguments in calls:
    print(f"CALL line={line_number} name={name} arguments={arguments}")
print(f"TRACE_SELECTED_MESSAGE_COUNT {len(messages)}")
for line_number, role, text in messages:
    if role != "user" or any(keyword in text for keyword in KEYWORDS):
        print(f"MESSAGE line={line_number} role={role} tail={text}")
