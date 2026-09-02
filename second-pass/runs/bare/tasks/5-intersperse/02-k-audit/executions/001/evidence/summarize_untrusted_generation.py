#!/usr/bin/env python3
"""Stream every byte/record of the large untrusted generation logs and summarize."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


plain_path = Path("/candidate/codex-output.log")
trace_path = next(Path("/candidate/codex-trace").rglob("*.jsonl"))


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


plain_counts = collections.Counter()
significant = collections.deque(maxlen=50)
with plain_path.open("r", encoding="utf-8", errors="replace") as stream:
    for number, line in enumerate(stream, 1):
        plain_counts["lines"] += 1
        for marker in (
            "kompile ",
            "krun ",
            "kprove ",
            "#Top",
            "WarnStuckClaimState",
            "RESULT:",
            "succeeded in",
            "exited ",
        ):
            if marker in line:
                plain_counts[marker] += 1
                significant.append((number, line.rstrip()[:500]))

top_types = collections.Counter()
payload_types = collections.Counter()
response_types = collections.Counter()
roles = collections.Counter()
trace_tail = collections.deque(maxlen=40)
record_count = 0
parse_errors = []
with trace_path.open("r", encoding="utf-8") as stream:
    for number, line in enumerate(stream, 1):
        record_count += 1
        try:
            record = json.loads(line)
        except Exception as error:  # pragma: no cover - audit diagnostic
            parse_errors.append((number, repr(error)))
            continue
        top_type = record.get("type", "<missing>")
        top_types[top_type] += 1
        payload = record.get("payload")
        if not isinstance(payload, dict):
            continue
        payload_type = payload.get("type", "<missing>")
        payload_types[payload_type] += 1
        if top_type == "response_item":
            response_types[payload_type] += 1
            role = payload.get("role")
            if role:
                roles[role] += 1
            if payload_type == "function_call":
                name = payload.get("name", "<unnamed>")
                arguments = str(payload.get("arguments", ""))
                trace_tail.append(
                    f"line {number}: call {name} args={arguments[:350]!r}"
                )
            elif payload_type == "function_call_output":
                output = str(payload.get("output", ""))
                trace_tail.append(
                    f"line {number}: call_output chars={len(output)} "
                    f"head={output[:180]!r} tail={output[-180:]!r}"
                )
            elif payload_type == "message" and role == "assistant":
                content = payload.get("content", [])
                texts = [
                    item.get("text", "")
                    for item in content
                    if isinstance(item, dict) and item.get("type") in {"output_text", "input_text"}
                ]
                joined = " ".join(texts)
                trace_tail.append(
                    f"line {number}: assistant_message chars={len(joined)} "
                    f"text={joined[:500]!r}"
                )

print(f"plain_path={plain_path}")
print(f"plain_bytes={plain_path.stat().st_size}")
print(f"plain_sha256={digest(plain_path)}")
print(f"plain_counts={dict(plain_counts)}")
print("plain_last_significant_lines:")
for item in significant:
    print(f"  {item!r}")
print(f"trace_path={trace_path}")
print(f"trace_bytes={trace_path.stat().st_size}")
print(f"trace_sha256={digest(trace_path)}")
print(f"trace_records={record_count}")
print(f"trace_parse_errors={parse_errors!r}")
print(f"trace_top_types={dict(top_types)}")
print(f"trace_payload_types={dict(payload_types)}")
print(f"trace_response_types={dict(response_types)}")
print(f"trace_roles={dict(roles)}")
print("trace_last_bounded_events:")
for item in trace_tail:
    print(f"  {item}")
