#!/usr/bin/env python3
"""Parse every record required by the declared legacy-selected-stage1 layout."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


json_records = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/usage.json"),
]
for path in json_records:
    doc = json.loads(path.read_text())
    print(
        "JSON",
        path,
        "sha256=" + digest(path),
        "schema=" + str(doc.get("schema_version")),
        "status=" + str(doc.get("status")),
        "stage=" + str(doc.get("stage") or doc.get("current_stage")),
        "marker=" + str(doc.get("result_marker")),
    )

for path in (
    Path("/generation-evidence/prompt.txt"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
):
    text = path.read_text(errors="replace")
    print(
        "TEXT",
        path,
        "sha256=" + digest(path),
        "lines=" + str(len(text.splitlines())),
        "bytes=" + str(len(text.encode())),
        "top_markers=" + str(text.count("#Top")),
        "passed_markers=" + str(text.count("RESULT: KPROVE_PASSED")),
    )
    if path.name == "codex-last.txt":
        print("CODEX_LAST", repr(text))

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
regular_trace_files = [path for path in trace_files if path.is_file()]
print("TRACE_FILES", [str(path) for path in regular_trace_files])
for path in regular_trace_files:
    counts: collections.Counter[str] = collections.Counter()
    tool_names: collections.Counter[str] = collections.Counter()
    parse_errors = []
    records = 0
    final_messages = []
    for line_number, line in enumerate(path.open(), 1):
        records += 1
        try:
            item = json.loads(line)
        except Exception as error:
            parse_errors.append([line_number, str(error)])
            continue
        counts[item.get("type", "?")] += 1
        payload = item.get("payload")
        if isinstance(payload, dict):
            payload_type = payload.get("type")
            if payload_type:
                counts["payload:" + payload_type] += 1
            if payload_type in {"function_call", "custom_tool_call"}:
                tool_names[str(payload.get("name"))] += 1
            if payload_type == "task_complete":
                final_messages.append(payload.get("last_agent_message"))
    print(
        "TRACE",
        path,
        "sha256=" + digest(path),
        "records=" + str(records),
        "parse_errors=" + repr(parse_errors),
    )
    print("TRACE_TYPES", json.dumps(counts, sort_keys=True))
    print("TRACE_TOOL_NAMES", json.dumps(tool_names, sort_keys=True))
    print("TRACE_FINAL_MESSAGES", json.dumps(final_messages, ensure_ascii=False))
