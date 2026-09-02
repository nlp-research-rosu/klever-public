#!/usr/bin/env python3
"""Validate and summarize every record in the untrusted generation JSONL trace."""

from __future__ import annotations

import collections
import json
from pathlib import Path


def compact(text: str, limit: int = 1800) -> str:
    text = text.replace("\r", "")
    if len(text) <= limit:
        return text
    half = limit // 2
    return text[:half] + "\n... bounded ...\n" + text[-half:]


def main() -> int:
    traces = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    print(f"trace_file_count={len(traces)}")
    for trace in traces:
        print(f"\nTRACE {trace}")
        top = collections.Counter()
        payloads = collections.Counter()
        calls = {}
        completed = set()
        lines = trace.read_text().splitlines()
        for number, line in enumerate(lines, 1):
            record = json.loads(line)
            top[record.get("type")] += 1
            payload = record.get("payload") or {}
            payload_type = payload.get("type")
            payloads[payload_type] += 1
            if payload_type in {"custom_tool_call", "function_call"}:
                call_id = payload.get("call_id")
                calls[call_id] = (number, payload.get("name"), payload.get("input"))
            elif payload_type in {"custom_tool_call_output", "function_call_output"}:
                call_id = payload.get("call_id")
                completed.add(call_id)
                call = calls.get(call_id)
                print(f"\nCALL/OUTPUT line={number} call={call}")
                print(compact(json.dumps(payload.get("output"), ensure_ascii=False)))
            elif payload_type == "patch_apply_end":
                print(
                    f"\nPATCH line={number} success={payload.get('success')} "
                    f"files={sorted((payload.get('changes') or {}).keys())}"
                )
            elif payload_type in {"agent_message", "task_complete"}:
                message = payload.get("message") or payload.get("last_agent_message")
                print(f"\nMESSAGE line={number} type={payload_type}")
                print(compact(str(message)))
        print(f"\nvalid_json_lines={len(lines)}")
        print(f"top_level_types={dict(top)}")
        print(f"payload_types={dict(payloads)}")
        print(f"unmatched_call_ids={sorted(set(calls) - completed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
