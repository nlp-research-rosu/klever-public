#!/usr/bin/env python3
"""Bounded independent inspection of every required legacy generation record."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


json_records = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/usage.json"),
    Path("/generation-evidence/legacy-run-input.json"),
    Path("/generation-evidence/legacy-metrics.json"),
]
for path in json_records:
    value = json.loads(path.read_text())
    print(
        f"JSON_OK path={path} schema_version={value.get('schema_version')} "
        f"status={value.get('status')} exit_code={value.get('exit_code')}"
    )

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
print(f"trace_file_count={len(trace_files)}")
for path in trace_files:
    counts: collections.Counter[tuple[object, object]] = collections.Counter()
    lines = 0
    last_final = None
    with path.open() as stream:
        for line_number, line in enumerate(stream, 1):
            event = json.loads(line)
            lines += 1
            payload = event.get("payload") or {}
            counts[(event.get("type"), payload.get("type"))] += 1
            if payload.get("type") in {"agent_message", "message"}:
                text = payload.get("message")
                if isinstance(text, str) and "RESULT:" in text:
                    last_final = text.splitlines()[-1]
    print(f"TRACE_JSONL_OK path={path} lines={lines}")
    for key, count in sorted(counts.items(), key=lambda item: repr(item[0])):
        print(f"TRACE_EVENT_COUNT outer={key[0]!r} inner={key[1]!r} count={count}")
    print(f"TRACE_LAST_RESULT_CLAIM={last_final!r}")

for path in [
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/prompt.txt"),
]:
    raw = path.read_bytes()
    text = raw.decode(errors="replace")
    print(
        f"TEXT_OK path={path} bytes={len(raw)} lines={len(text.splitlines())} "
        f"sha256={hashlib.sha256(raw).hexdigest()} "
        f"top_markers={text.count('#Top')} "
        f"kprove_mentions={text.lower().count('kprove')} "
        f"result_markers={text.count('RESULT:')}"
    )
    if path.name == "codex-last.txt":
        print("CODEX_LAST_BEGIN")
        print(text.rstrip())
        print("CODEX_LAST_END")
