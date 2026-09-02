#!/usr/bin/env python3
"""Parse every structured generation-trace line and summarize untrusted claims."""

from __future__ import annotations

import collections
import json
from pathlib import Path


def compact(value: object, limit: int) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    return " ".join(text.split())[:limit]


def main() -> int:
    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    if not trace_files:
        print("ERROR: no structured JSONL traces")
        return 1

    top_types: collections.Counter[str] = collections.Counter()
    response_types: collections.Counter[str] = collections.Counter()
    event_types: collections.Counter[str] = collections.Counter()
    calls: list[str] = []
    outputs: list[str] = []
    messages: list[str] = []
    total_lines = 0

    for trace in trace_files:
        print(f"TRACE {trace}")
        with trace.open() as stream:
            for line_number, line in enumerate(stream, 1):
                total_lines += 1
                record = json.loads(line)
                top_type = record.get("type", "<none>")
                top_types[top_type] += 1
                payload = record.get("payload", {})
                if top_type == "response_item":
                    subtype = payload.get("type", "<none>")
                    response_types[subtype] += 1
                    if subtype == "function_call":
                        calls.append(
                            f"{line_number}: {payload.get('name')} "
                            f"{compact(payload.get('arguments', ''), 600)}"
                        )
                    elif subtype == "function_call_output":
                        outputs.append(
                            f"{line_number}: {compact(payload.get('output', ''), 250)}"
                        )
                    elif subtype == "message":
                        messages.append(
                            f"{line_number}: role={payload.get('role')} "
                            f"{compact(payload.get('content', ''), 500)}"
                        )
                elif top_type == "event_msg":
                    subtype = payload.get("type", "<none>")
                    event_types[subtype] += 1

    print(f"parsed_jsonl_lines={total_lines}")
    print(f"top_types={dict(sorted(top_types.items()))}")
    print(f"response_item_types={dict(sorted(response_types.items()))}")
    print(f"event_payload_types={dict(sorted(event_types.items()))}")
    print(f"function_call_count={len(calls)}")
    for item in calls:
        print(f"CALL {item}")
    print(f"function_output_count={len(outputs)}")
    for item in outputs:
        print(f"OUTPUT {item}")
    print(f"message_count={len(messages)}")
    for item in messages:
        print(f"MESSAGE {item}")

    output_log = Path("/generation-evidence/codex-output.log")
    data = output_log.read_text(errors="replace")
    print(f"codex_output_chars={len(data)}")
    print(f"codex_output_lines={len(data.splitlines())}")
    probes = [
        "#Top",
        "WarnStuckClaimState",
        "error:",
        "RESULT:",
        "kprove spec.k",
        "kompile verification.k",
        "countUpperFrom",
    ]
    for probe in probes:
        print(f"codex_output_count[{probe!r}]={data.count(probe)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
