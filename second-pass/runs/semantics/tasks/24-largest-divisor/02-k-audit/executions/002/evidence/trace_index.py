#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def compact(value: object, limit: int = 500) -> str:
    text = json.dumps(value, sort_keys=True, ensure_ascii=False)
    text = " ".join(text.split())
    if len(text) > limit:
        text = text[:limit] + "…"
    return text.replace("\t", " ")


def main() -> None:
    trace_root = Path("/generation-evidence/codex-trace")
    output = Path("/audit-output/evidence/generation-trace-index.tsv")
    rows = [
        "file\tline\ttimestamp\trecord_type\tpayload_type\tname_or_phase"
        "\tcall_id\tpayload_sha256\tbounded_summary"
    ]
    count = 0
    for path in sorted(trace_root.rglob("*.jsonl")):
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                if not line.strip():
                    continue
                document = json.loads(line)
                payload = document.get("payload")
                if not isinstance(payload, dict):
                    payload = {}
                payload_bytes = json.dumps(
                    payload,
                    sort_keys=True,
                    separators=(",", ":"),
                    ensure_ascii=False,
                ).encode()
                record_type = str(document.get("type", ""))
                payload_type = str(payload.get("type", ""))
                name_or_phase = str(
                    payload.get("name", payload.get("phase", ""))
                )
                call_id = str(
                    payload.get("call_id", payload.get("id", ""))
                )
                if payload_type in {
                    "function_call",
                    "custom_tool_call",
                    "function_call_output",
                    "custom_tool_call_output",
                    "agent_message",
                    "message",
                }:
                    summary = compact(payload)
                else:
                    summary = compact(
                        {
                            key: payload.get(key)
                            for key in (
                                "type",
                                "turn_id",
                                "status",
                                "duration_ms",
                            )
                            if key in payload
                        }
                    )
                rows.append(
                    "\t".join(
                        [
                            path.relative_to(trace_root).as_posix(),
                            str(line_number),
                            str(document.get("timestamp", "")),
                            record_type,
                            payload_type,
                            name_or_phase,
                            call_id,
                            hashlib.sha256(payload_bytes).hexdigest(),
                            summary,
                        ]
                    )
                )
                count += 1
    output.write_text("\n".join(rows) + "\n")
    print(f"trace_index={output}")
    print(f"indexed_json_objects={count}")
    print("TRACE_INDEX=PASS")


if __name__ == "__main__":
    main()
