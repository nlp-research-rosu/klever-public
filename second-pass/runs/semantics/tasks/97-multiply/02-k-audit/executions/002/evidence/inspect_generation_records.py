#!/usr/bin/env python3
"""Parse every required legacy-selected-stage1 record and trace event."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


json_records = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/usage.json"),
]
text_records = [
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]

print("JSON_RECORDS")
for path in json_records:
    if path.is_symlink() or not path.is_file():
        raise AssertionError(f"not a regular record: {path}")
    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise AssertionError(f"not a JSON object: {path}")
    print(
        f"{path} bytes={path.stat().st_size} sha256={sha(path)} "
        f"top_keys={','.join(sorted(document))}"
    )

print("TEXT_RECORDS")
for path in text_records:
    if path.is_symlink() or not path.is_file():
        raise AssertionError(f"not a regular record: {path}")
    text = path.read_text(encoding="utf-8")
    print(
        f"{path} bytes={len(text.encode())} lines={len(text.splitlines())} "
        f"sha256={sha(path)}"
    )
    if path.name == "codex-last.txt":
        print("codex_last_final_line=" + text.splitlines()[-1])
    if path.name == "codex-output.log":
        print("codex_output_has_success_marker=" + str("RESULT: KPROVE_PASSED" in text))

trace_root = Path("/generation-evidence/codex-trace")
trace_files = sorted(trace_root.rglob("*.jsonl"))
if not trace_files:
    raise AssertionError("structured trace has no JSONL files")
print("STRUCTURED_TRACE")
event_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
tool_names: Counter[str] = Counter()
session_ids: set[str] = set()
total_events = 0
for path in trace_files:
    relative = path.relative_to(trace_root)
    events = []
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        try:
            event = json.loads(line)
        except json.JSONDecodeError as error:
            raise AssertionError(f"{relative}:{line_number}: {error}") from error
        if not isinstance(event, dict):
            raise AssertionError(f"{relative}:{line_number}: non-object event")
        events.append(event)
        event_types[str(event.get("type"))] += 1
        payload = event.get("payload")
        if isinstance(payload, dict):
            payload_type = payload.get("type")
            if payload_type is not None:
                payload_types[str(payload_type)] += 1
            if event.get("type") == "session_meta":
                session = payload.get("session_id")
                if isinstance(session, str):
                    session_ids.add(session)
            name = payload.get("name")
            if isinstance(name, str) and (
                payload_type in {"custom_tool_call", "function_call"}
                or event.get("type") in {"custom_tool_call", "function_call"}
            ):
                tool_names[name] += 1
    total_events += len(events)
    print(
        f"{relative} events={len(events)} bytes={path.stat().st_size} "
        f"sha256={sha(path)} first_type={events[0].get('type')} "
        f"last_type={events[-1].get('type')}"
    )

print(f"trace_files={len(trace_files)}")
print(f"trace_events={total_events}")
print("event_types=" + json.dumps(event_types, sort_keys=True))
print("payload_types=" + json.dumps(payload_types, sort_keys=True))
print("tool_names=" + json.dumps(tool_names, sort_keys=True))
print("session_ids=" + json.dumps(sorted(session_ids)))

invocation = json.loads(
    Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
)
expected_trace = invocation["outputs"]["evidence"]
for relative, expected_hash in sorted(expected_trace.items()):
    if not relative.startswith("codex-trace/"):
        continue
    mounted = Path("/generation-evidence") / relative
    actual_hash = sha(mounted)
    match = actual_hash == expected_hash
    print(
        f"trace_record_hash {relative} expected={expected_hash} "
        f"actual={actual_hash} match={match}"
    )
    if not match:
        raise AssertionError(f"trace hash mismatch: {relative}")

print("all_generation_records_parse=True")
