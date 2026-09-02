#!/usr/bin/env python3
"""Parse every generation trace record and summarize untrusted actions."""

from __future__ import annotations

import json
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")


def compact(value: str, limit: int = 1200) -> str:
    value = value.replace("\n", "\\n")
    if len(value) <= limit:
        return value
    return value[:limit] + f"...<truncated {len(value) - limit} chars>"


def main() -> None:
    serial = 0
    for trace_path in sorted(TRACE_ROOT.rglob("*.jsonl")):
        print(f"TRACE_FILE {trace_path}")
        with trace_path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                serial += 1
                record = json.loads(line)
                payload = record.get("payload", {})
                record_type = record.get("type")
                if record_type == "response_item":
                    payload_type = payload.get("type")
                    if payload_type == "function_call":
                        raw_arguments = payload.get("arguments", "")
                        try:
                            arguments = json.loads(raw_arguments)
                        except (json.JSONDecodeError, TypeError):
                            arguments = {"raw": raw_arguments}
                        print(
                            f"CALL line={line_number} name={payload.get('name')} "
                            f"arguments={compact(json.dumps(arguments, sort_keys=True))}"
                        )
                    elif payload_type == "custom_tool_call":
                        print(
                            f"CUSTOM_CALL line={line_number} "
                            f"name={payload.get('name')} "
                            f"input={compact(str(payload.get('input', '')))}"
                        )
                    elif payload_type == "message":
                        role = payload.get("role")
                        texts = []
                        for item in payload.get("content", []):
                            if isinstance(item, dict) and "text" in item:
                                texts.append(str(item["text"]))
                        if role in {"assistant", "user"}:
                            print(
                                f"MESSAGE line={line_number} role={role} "
                                f"text={compact(' '.join(texts))}"
                            )
                elif record_type == "event_msg":
                    subtype = payload.get("type")
                    if subtype in {"task_started", "task_complete", "agent_message"}:
                        print(
                            f"EVENT line={line_number} subtype={subtype} "
                            f"payload={compact(json.dumps(payload, sort_keys=True))}"
                        )
    print(f"PARSED_JSON_RECORDS {serial}")


if __name__ == "__main__":
    main()
