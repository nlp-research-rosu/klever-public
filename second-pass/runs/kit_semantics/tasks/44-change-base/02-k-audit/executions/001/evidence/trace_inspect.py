#!/usr/bin/env python3
import collections
import glob
import hashlib
import json
from pathlib import Path


paths = sorted(glob.glob("/generation-evidence/codex-trace/**/*.jsonl", recursive=True))
print(f"trace_files={len(paths)}")
all_calls = {}
all_outputs = set()
failures = []

for raw_path in paths:
    path = Path(raw_path)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    top_counts = collections.Counter()
    payload_counts = collections.Counter()
    line_count = 0
    for line_count, line in enumerate(path.open(), 1):
        try:
            event = json.loads(line)
        except Exception as err:
            failures.append(f"{path}:{line_count}: malformed JSON: {err}")
            continue
        top_counts[event.get("type")] += 1
        payload = event.get("payload")
        payload_type = payload.get("type") if isinstance(payload, dict) else None
        payload_counts[payload_type] += 1
        if payload_type in {"function_call", "custom_tool_call"}:
            call_id = payload.get("call_id")
            all_calls[call_id] = (path, line_count, payload.get("name"))
            arguments = payload.get("arguments", payload.get("input", ""))
            if payload.get("name") in {
                "exec_command",
                "write_stdin",
                "apply_patch",
            }:
                compact = " ".join(str(arguments).split())
                print(
                    f"CALL {path.name}:{line_count} id={call_id} "
                    f"name={payload.get('name')} args={compact[:500]}"
                )
        if payload_type in {"function_call_output", "custom_tool_call_output"}:
            all_outputs.add(payload.get("call_id"))
        if payload_type in {"agent_message", "task_complete"}:
            message = payload.get("message", payload.get("last_agent_message", ""))
            if "#Top" in message or "RESULT:" in message or "Gate" in message:
                compact = " ".join(message.split())
                print(f"CLAIM {path.name}:{line_count}: {compact[:700]}")
    print(
        f"TRACE {path}: sha256={digest} lines={line_count} "
        f"top_types={dict(top_counts)} payload_types={dict(payload_counts)}"
    )

missing_outputs = sorted(str(call_id) for call_id in all_calls if call_id not in all_outputs)
orphan_outputs = sorted(str(call_id) for call_id in all_outputs if call_id not in all_calls)
print(f"calls={len(all_calls)} outputs={len(all_outputs)}")
print(f"missing_call_outputs={missing_outputs}")
print(f"orphan_call_outputs={orphan_outputs}")

log_path = Path("/generation-evidence/codex-output.log")
print(
    f"codex_output sha256={hashlib.sha256(log_path.read_bytes()).hexdigest()} "
    f"bytes={log_path.stat().st_size}"
)
last_path = Path("/generation-evidence/codex-last.txt")
print(
    f"codex_last sha256={hashlib.sha256(last_path.read_bytes()).hexdigest()} "
    f"bytes={last_path.stat().st_size}"
)
print(f"FAILURE_COUNT={len(failures)}")
for failure in failures:
    print(f"FAILURE: {failure}")
raise SystemExit(1 if failures else 0)
