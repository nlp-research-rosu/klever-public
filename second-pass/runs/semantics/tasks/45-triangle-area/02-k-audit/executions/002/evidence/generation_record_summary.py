#!/usr/bin/env python3
"""Parse every legacy-selected-stage1 generation record and trace event."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


json_records = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/usage.json"),
]
for path in json_records:
    document = json.loads(path.read_text())
    print(
        f"parsed_json={path} schema_version={document.get('schema_version')} "
        f"status={document.get('status', 'n/a')}"
    )

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
trace_files = [path for path in trace_files if path.is_file()]
print(f"trace_file_count={len(trace_files)}")
event_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
session_ids: set[str] = set()
line_count = 0
for path in trace_files:
    with path.open() as stream:
        for raw_line in stream:
            line_count += 1
            event = json.loads(raw_line)
            event_types[str(event.get("type"))] += 1
            payload = event.get("payload")
            if isinstance(payload, dict):
                payload_types[str(payload.get("type"))] += 1
                for key in ("session_id", "id"):
                    value = payload.get(key)
                    if isinstance(value, str) and len(value) == 36:
                        session_ids.add(value)
print(f"trace_json_line_count={line_count}")
print(f"trace_event_types={dict(sorted(event_types.items()))}")
print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
print(f"trace_session_ids={sorted(session_ids)}")

output = Path("/generation-evidence/codex-output.log").read_text(errors="replace")
last = Path("/generation-evidence/codex-last.txt").read_text(errors="replace")
prompt = Path("/generation-evidence/prompt.txt").read_text(errors="replace")
print(f"codex_output_line_count={len(output.splitlines())}")
print(f"codex_output_kprove_mentions={output.count('kprove')}")
print(f"codex_output_top_mentions={output.count('#Top')}")
print(f"codex_output_error_mentions={output.count('[Error]')}")
print(f"codex_last_line_count={len(last.splitlines())}")
print(f"generation_prompt_line_count={len(prompt.splitlines())}")
print(f"final_marker_present={'RESULT: KPROVE_PASSED' in last}")
print("GENERATION_RECORD_PARSE=PASS")
