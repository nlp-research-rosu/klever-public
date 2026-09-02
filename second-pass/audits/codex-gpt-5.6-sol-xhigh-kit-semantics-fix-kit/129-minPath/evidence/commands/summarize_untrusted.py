#!/usr/bin/env python3
"""Parse the entire untrusted generation record and emit a bounded summary."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


CANDIDATE = Path("/candidate")
TRACE = next((CANDIDATE / "codex-trace").rglob("*.jsonl"))


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


for name in ("run-input.json", "metrics.json"):
    path = CANDIDATE / name
    with path.open(encoding="utf-8") as stream:
        value = json.load(stream)
    print(f"{name}: valid JSON; sha256={digest(path)}")
    print(json.dumps(value, sort_keys=True))

for name in ("codex-last.txt", "codex-output.log"):
    path = CANDIDATE / name
    text = path.read_text(encoding="utf-8", errors="replace")
    claims = collections.Counter()
    for marker in (
        "#Top",
        "WarnStuckClaimState",
        "SOUND-BUT-LIMITED",
        "KPROVE_PASSED",
        "EXPECTED FAILURE",
    ):
        claims[marker] = text.count(marker)
    print(
        f"{name}: bytes={path.stat().st_size}; sha256={digest(path)}; "
        f"untrusted_marker_counts={dict(claims)}"
    )
    if name == "codex-last.txt":
        print(text.rstrip())

event_counts: collections.Counter[str] = collections.Counter()
payload_counts: collections.Counter[str] = collections.Counter()
assistant_finals: list[str] = []
line_count = 0
with TRACE.open(encoding="utf-8") as stream:
    for line_count, line in enumerate(stream, 1):
        record = json.loads(line)
        event_counts[str(record.get("type"))] += 1
        payload = record.get("payload")
        if isinstance(payload, dict):
            payload_counts[str(payload.get("type"))] += 1
            if (
                record.get("type") == "response_item"
                and payload.get("type") == "message"
                and payload.get("role") == "assistant"
                and payload.get("phase") == "final_answer"
            ):
                parts = payload.get("content", [])
                assistant_finals.append(
                    "".join(
                        str(part.get("text", ""))
                        for part in parts
                        if isinstance(part, dict)
                    )
                )

print(
    f"trace: path={TRACE}; lines={line_count}; bytes={TRACE.stat().st_size}; "
    f"sha256={digest(TRACE)}"
)
print(f"trace_event_counts={dict(sorted(event_counts.items()))}")
print(f"trace_payload_type_counts={dict(sorted(payload_counts.items()))}")
print(f"trace_final_assistant_messages={len(assistant_finals)}")
for index, message in enumerate(assistant_finals, 1):
    print(f"trace_final_{index}={message.rstrip()}")
