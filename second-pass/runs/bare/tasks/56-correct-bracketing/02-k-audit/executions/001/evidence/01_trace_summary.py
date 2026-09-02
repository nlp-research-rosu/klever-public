#!/usr/bin/env python3
"""Summarize the untrusted structured generation trace for provenance review."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE_ROOT = Path("/candidate/codex-trace")


def main() -> int:
    trace_files = sorted(TRACE_ROOT.rglob("*.jsonl"))
    print(f"trace_files={len(trace_files)}")
    for path in trace_files:
        type_counts: collections.Counter[str] = collections.Counter()
        payload_counts: collections.Counter[str] = collections.Counter()
        malformed = 0
        records = 0
        final_messages: list[str] = []
        command_results: collections.Counter[str] = collections.Counter()
        with path.open(encoding="utf-8") as stream:
            for line in stream:
                records += 1
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    malformed += 1
                    continue
                type_counts[str(record.get("type"))] += 1
                payload = record.get("payload")
                if isinstance(payload, dict):
                    payload_type = str(payload.get("type"))
                    payload_counts[payload_type] += 1
                    if payload_type == "agent_message":
                        message = payload.get("message")
                        if isinstance(message, str) and "RESULT:" in message:
                            final_messages.append(message.replace("\n", " | "))
                    if payload_type in {"function_call_output", "command_execution"}:
                        command_results[str(payload.get("status"))] += 1
        print(f"path={path}")
        print(f"records={records} malformed_json_lines={malformed}")
        print(f"record_types={dict(sorted(type_counts.items()))}")
        print(f"payload_types={dict(sorted(payload_counts.items()))}")
        print(f"command_statuses={dict(sorted(command_results.items()))}")
        for message in final_messages:
            print(f"untrusted_result_claim={message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
