#!/usr/bin/env python3
"""Parse every structured-trace record and summarize untrusted generation activity."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


root = Path("/generation-evidence/codex-trace")
files = sorted(root.rglob("*"))
trace_files = [path for path in files if path.is_file() and not path.is_symlink()]
if not trace_files:
    raise SystemExit("no trace files")

counts: Counter[str] = Counter()
records = 0
tool_summaries: list[str] = []
message_summaries: list[str] = []

for path in trace_files:
    raw = path.read_bytes()
    print(
        f"TRACE_FILE {path.relative_to(root)} bytes={len(raw)} "
        f"sha256={hashlib.sha256(raw).hexdigest()}"
    )
    for line_number, line in enumerate(raw.splitlines(), 1):
        obj = json.loads(line)
        records += 1
        top_type = str(obj.get("type", "<none>"))
        payload = obj.get("payload")
        payload_type = payload.get("type", "<none>") if isinstance(payload, dict) else "<none>"
        counts[f"{top_type}/{payload_type}"] += 1

        if isinstance(payload, dict):
            name = payload.get("name")
            arguments = payload.get("arguments")
            if name is not None or arguments is not None:
                summary = f"line={line_number} name={name!r} arguments={arguments!r}"
                tool_summaries.append(summary[:1000])

            role = payload.get("role")
            content = payload.get("content")
            if role is not None and content is not None:
                rendered = json.dumps(content, sort_keys=True, ensure_ascii=False)
                content_hash = hashlib.sha256(rendered.encode()).hexdigest()
                message_summaries.append(
                    f"line={line_number} role={role!r} chars={len(rendered)} "
                    f"sha256={content_hash} prefix={rendered[:240]!r}"
                )

print(f"PARSED_RECORDS={records}")
for key, value in sorted(counts.items()):
    print(f"EVENT_COUNT {key}={value}")
print(f"TOOL_SUMMARIES={len(tool_summaries)}")
for item in tool_summaries:
    print(f"TOOL {item}")
print(f"MESSAGE_SUMMARIES={len(message_summaries)}")
for item in message_summaries:
    print(f"MESSAGE {item}")
