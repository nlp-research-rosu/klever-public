#!/usr/bin/env python3
"""Parse every structured generation trace record and summarize untrusted claims."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/23/"
    "rollout-2026-07-23T02-11-34-019f8dd0-b9b0-7f80-951f-e1dd2fd9eb01.jsonl"
)


def brief(value: object, limit: int = 260) -> str:
    text = json.dumps(value, sort_keys=True, ensure_ascii=False)
    text = " ".join(text.split())
    return text if len(text) <= limit else text[:limit] + "…"


def main() -> None:
    type_counts: collections.Counter[str] = collections.Counter()
    payload_counts: collections.Counter[str] = collections.Counter()
    calls: list[dict[str, object]] = []
    messages: list[dict[str, object]] = []
    last_record: dict[str, object] | None = None
    line_count = 0
    with TRACE.open() as stream:
        for line_count, line in enumerate(stream, 1):
            record = json.loads(line)
            assert isinstance(record, dict)
            last_record = record
            record_type = str(record.get("type"))
            type_counts[record_type] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_type = str(payload.get("type"))
                payload_counts[f"{record_type}/{payload_type}"] += 1
                if payload_type in {"function_call", "custom_tool_call"}:
                    calls.append(
                        {
                            "line": line_count,
                            "kind": payload_type,
                            "name": payload.get("name"),
                            "arguments": brief(payload.get("arguments") or payload.get("input")),
                        }
                    )
                elif payload_type == "function_call_output":
                    calls.append(
                        {
                            "line": line_count,
                            "kind": payload_type,
                            "call_id": payload.get("call_id"),
                            "output_sha256": hashlib.sha256(
                                str(payload.get("output", "")).encode()
                            ).hexdigest(),
                            "output_brief": brief(payload.get("output")),
                        }
                    )
                elif payload_type in {"message", "agent_message", "task_complete"}:
                    messages.append(
                        {
                            "line": line_count,
                            "kind": payload_type,
                            "brief": brief(payload),
                        }
                    )

    assert line_count == 207
    assert last_record is not None
    print(f"trace={TRACE}")
    print(f"trace_sha256={hashlib.sha256(TRACE.read_bytes()).hexdigest()}")
    print(f"parsed_jsonl_lines={line_count}")
    print(f"top_level_counts={dict(sorted(type_counts.items()))}")
    print(f"payload_counts={dict(sorted(payload_counts.items()))}")
    print(f"call_records={len(calls)}")
    for item in calls:
        print(brief(item, 720))
    print(f"message_records={len(messages)}")
    for item in messages:
        print(brief(item, 720))
    print(f"last_record={brief(last_record, 720)}")

    for path in [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/usage.json"),
    ]:
        document = json.loads(path.read_text())
        print(f"json_record {path} {brief(document, 900)}")
    for path in [
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/prompt.txt"),
        Path("/generation-evidence/codex-output.log"),
    ]:
        data = path.read_bytes()
        print(
            f"text_record {path} bytes={len(data)} "
            f"sha256={hashlib.sha256(data).hexdigest()}"
        )
    print("GENERATION_RECORDS_PARSED")


if __name__ == "__main__":
    main()
