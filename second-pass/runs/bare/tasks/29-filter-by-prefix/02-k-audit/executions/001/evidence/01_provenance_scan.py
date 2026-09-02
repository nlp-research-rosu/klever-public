#!/usr/bin/env python3
"""Read all provenance inputs as untrusted claims and print a bounded summary."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


CANDIDATE = Path("/candidate")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


for name in ("run-input.json", "metrics.json"):
    path = CANDIDATE / name
    print(f"FILE {path} sha256={digest(path)}")
    print(json.dumps(json.loads(path.read_text()), sort_keys=True))

for name in ("codex-last.txt", "codex-output.log"):
    path = CANDIDATE / name
    text = path.read_text(errors="replace")
    print(
        f"FILE {path} sha256={digest(path)} bytes={len(text.encode())} "
        f"lines={len(text.splitlines())}"
    )
    print(f"contains_top={('#Top' in text)}")
    print(f"contains_pass_marker={('RESULT: KPROVE_PASSED' in text)}")
    if name == "codex-last.txt":
        print(text.rstrip())

trace_paths = sorted((CANDIDATE / "codex-trace").rglob("*.jsonl"))
print(f"TRACE_FILES {len(trace_paths)}")
for path in trace_paths:
    outer_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    command_mentions: list[str] = []
    records = 0
    parse_errors = 0
    final_messages: list[str] = []
    with path.open(errors="replace") as stream:
        for line in stream:
            records += 1
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                parse_errors += 1
                continue
            outer_types[str(item.get("type"))] += 1
            payload = item.get("payload")
            if isinstance(payload, dict):
                payload_types[str(payload.get("type"))] += 1
                serialized = json.dumps(payload, ensure_ascii=False)
                if any(word in serialized for word in ("kompile", "kprove", "krun")):
                    if len(command_mentions) < 20:
                        command_mentions.append(serialized[:500])
                if payload.get("phase") == "final_answer":
                    for content in payload.get("content", []):
                        if isinstance(content, dict) and isinstance(content.get("text"), str):
                            final_messages.append(content["text"])
    print(
        f"TRACE {path} sha256={digest(path)} records={records} "
        f"parse_errors={parse_errors}"
    )
    print(f"outer_types={dict(sorted(outer_types.items()))}")
    print(f"payload_types={dict(sorted(payload_types.items()))}")
    print(f"bounded_tool_mentions={len(command_mentions)}")
    for mention in command_mentions:
        print(f"MENTION {mention}")
    for message in final_messages:
        print(f"FINAL_CLAIM {message}")
