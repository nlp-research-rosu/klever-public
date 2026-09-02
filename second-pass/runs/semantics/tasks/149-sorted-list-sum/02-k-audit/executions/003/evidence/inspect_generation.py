#!/usr/bin/env python3
"""Bounded structural inspection of untrusted generation records."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/23/"
    "rollout-2026-07-23T07-25-39-019f8ef0-47f7-7810-afd7-b9eb0c1a4a81.jsonl"
)
RAW_LOG = Path("/generation-evidence/codex-output.log")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def shorten(value: object, limit: int = 800) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    text = text.replace("\n", "\\n")
    return text if len(text) <= limit else text[:limit] + "...<TRUNCATED>"


lines = TRACE.read_text(encoding="utf-8").splitlines()
records = [json.loads(line) for line in lines]
print(f"trace_path={TRACE}")
print(f"trace_lines={len(records)} trace_sha256={sha256(TRACE)}")
print("top_level_types=" + repr(collections.Counter(r.get("type") for r in records)))

payload_types: collections.Counter[str] = collections.Counter()
function_calls: list[tuple[int, str, object]] = []
messages: list[tuple[int, str, str, str]] = []
events: list[tuple[int, str]] = []

for number, record in enumerate(records, 1):
    payload = record.get("payload", {})
    ptype = payload.get("type", "<none>")
    payload_types[ptype] += 1
    if record.get("type") == "event_msg":
        events.append((number, ptype))
    if ptype in {"function_call", "custom_tool_call"}:
        function_calls.append(
            (number, payload.get("name", "<unnamed>"), payload.get("arguments", payload.get("input")))
        )
    if ptype == "message":
        role = payload.get("role", "<none>")
        phase = payload.get("phase", "")
        text_parts = []
        for item in payload.get("content", []):
            if isinstance(item, dict) and "text" in item:
                text_parts.append(item["text"])
        messages.append((number, role, phase, "\n".join(text_parts)))

print("payload_types=" + repr(payload_types))
print("event_sequence=" + repr(events))
print(f"function_call_count={len(function_calls)}")
for number, name, arguments in function_calls:
    print(f"CALL line={number} name={name} args={shorten(arguments)}")

print(f"message_count={len(messages)}")
for number, role, phase, text in messages:
    digest = hashlib.sha256(text.encode()).hexdigest()
    print(
        f"MESSAGE line={number} role={role} phase={phase} "
        f"chars={len(text)} sha256={digest} text={shorten(text)}"
    )

raw = RAW_LOG.read_text(encoding="utf-8", errors="replace")
raw_lines = raw.splitlines()
print(f"raw_log_path={RAW_LOG}")
print(f"raw_log_lines={len(raw_lines)} raw_log_chars={len(raw)} raw_log_sha256={sha256(RAW_LOG)}")
needles = (
    "kompile",
    "kprove",
    "krun",
    "apply_patch",
    "solution.py",
    "solution.mpy",
    "verification.k",
    "spec.k",
    "prove.sh",
    "#Top",
    "WarnStuckClaimState",
    "RESULT:",
)
for number, line in enumerate(raw_lines, 1):
    if any(needle in line for needle in needles):
        print(f"RAW line={number} text={shorten(line, 1200)}")
