#!/usr/bin/env python3
"""Bounded structural summary of untrusted generation logs and trace."""

from __future__ import annotations

import collections
import glob
import hashlib
import json
from pathlib import Path


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


for raw in (
    "/candidate/run-input.json",
    "/candidate/metrics.json",
    "/candidate/codex-last.txt",
    "/candidate/codex-output.log",
):
    path = Path(raw)
    data = path.read_bytes()
    print(
        f"artifact={path} bytes={len(data)} lines={data.count(bytes([10]))} "
        f"sha256={digest(path)}"
    )

print("\n--- codex-last.txt (untrusted claim) ---")
print(Path("/candidate/codex-last.txt").read_text(), end="")

print("\n--- codex-output.log keyword scan (untrusted claims, bounded excerpts) ---")
keywords = (
    "#Top",
    "WarnStuckClaimState",
    "prove.sh",
    "exhaustive",
    "RESULT:",
    "krun iscube",
)
counts = collections.Counter()
excerpts = []
with Path("/candidate/codex-output.log").open(errors="replace") as stream:
    for line_number, line in enumerate(stream, 1):
        matched = [keyword for keyword in keywords if keyword in line]
        for keyword in matched:
            counts[keyword] += line.count(keyword)
        if matched:
            excerpts.append((line_number, line.rstrip()[:500]))
for keyword in keywords:
    print(f"{keyword!r}: occurrences={counts[keyword]}")
for line_number, excerpt in excerpts[-60:]:
    print(f"{line_number}: {excerpt}")

print("\n--- structured trace validation and final claims ---")
trace_paths = [Path(path) for path in glob.glob("/candidate/codex-trace/**/*.jsonl", recursive=True)]
print(f"trace_file_count={len(trace_paths)}")
for path in trace_paths:
    outer_types = collections.Counter()
    response_types = collections.Counter()
    event_types = collections.Counter()
    parsed = 0
    task_completions = []
    assistant_messages = []
    with path.open() as stream:
        for line in stream:
            obj = json.loads(line)
            parsed += 1
            outer_types[obj.get("type")] += 1
            payload = obj.get("payload", {})
            if obj.get("type") == "response_item":
                response_types[payload.get("type")] += 1
                if payload.get("type") == "message" and payload.get("role") == "assistant":
                    text = "\n".join(
                        item.get("text", "")
                        for item in payload.get("content", [])
                        if isinstance(item, dict)
                    )
                    assistant_messages.append(text)
            elif obj.get("type") == "event_msg":
                event_types[payload.get("type")] += 1
                if payload.get("type") == "task_complete":
                    task_completions.append(payload.get("last_agent_message", ""))
    print(
        f"path={path} lines_parsed={parsed} bytes={path.stat().st_size} "
        f"sha256={digest(path)}"
    )
    print(f"outer_types={dict(outer_types)}")
    print(f"response_types={dict(response_types)}")
    print(f"event_types={dict(event_types)}")
    print(f"assistant_message_count={len(assistant_messages)}")
    print(f"task_completion_count={len(task_completions)}")
    for completion in task_completions:
        print("task_complete_claim=" + repr(completion))

