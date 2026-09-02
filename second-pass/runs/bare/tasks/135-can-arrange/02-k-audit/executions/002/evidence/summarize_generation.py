#!/usr/bin/env python3
"""Parse every structured generation-trace event and summarize its claims."""

from __future__ import annotations

import collections
import glob
import json
from pathlib import Path


def text_blocks(content: object) -> str:
    if not isinstance(content, list):
        return ""
    pieces = []
    for block in content:
        if isinstance(block, dict) and isinstance(block.get("text"), str):
            pieces.append(block["text"])
    return "\n".join(pieces)


def main() -> int:
    paths = sorted(glob.glob("/generation-evidence/codex-trace/**/*.jsonl", recursive=True))
    print(f"TRACE_FILES {len(paths)}")
    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    parsed = 0
    calls: dict[str, tuple[int, str, str]] = {}
    output_pairs = 0
    for trace_name in paths:
        path = Path(trace_name)
        print(f"TRACE {path} bytes={path.stat().st_size}")
        with path.open() as stream:
            for line_number, line in enumerate(stream, 1):
                record = json.loads(line)
                parsed += 1
                record_type = str(record.get("type"))
                top_types[record_type] += 1
                payload = record.get("payload")
                payload_type = (
                    str(payload.get("type")) if isinstance(payload, dict) else "<none>"
                )
                payload_types[payload_type] += 1
                if record_type != "response_item" or not isinstance(payload, dict):
                    continue
                if payload_type in {"function_call", "custom_tool_call"}:
                    call_id = str(payload.get("call_id"))
                    calls[call_id] = (
                        line_number,
                        str(payload.get("name")),
                        str(payload.get("arguments", payload.get("input"))),
                    )
                elif payload_type in {"custom_tool_call_output", "function_call_output"}:
                    call_id = str(payload.get("call_id"))
                    line_call = calls.get(call_id)
                    raw_output = payload.get("output")
                    output = (
                        text_blocks(raw_output)
                        if isinstance(raw_output, list)
                        else str(raw_output)
                    )
                    if line_call:
                        call_line, name, arguments = line_call
                        print(
                            f"CALL line={call_line} output_line={line_number} "
                            f"name={name} arguments={arguments}"
                        )
                        relevant = [
                            item
                            for item in output.splitlines()
                            if (
                                item.startswith("Process exited")
                                or "Process exited with code" in item
                                or item.strip() == "#Top"
                                or "WarnStuckClaimState" in item
                                or "[Error]" in item
                                or "timed out" in item.lower()
                                or item.startswith("<generatedTop>")
                                or item.strip().startswith("<k>")
                                or "Success. Updated" in item
                            )
                        ]
                        if not relevant:
                            relevant = output.splitlines()[-3:]
                        for item in relevant[:30]:
                            print(f"  OUTPUT {item[:1000]}")
                        if len(relevant) > 30:
                            print(f"  OUTPUT_OMITTED_RELEVANT count={len(relevant) - 30}")
                        output_pairs += 1
                elif payload_type == "message" and payload.get("role") == "assistant":
                    message = text_blocks(payload.get("content"))
                    if message:
                        print(f"ASSISTANT_MESSAGE line={line_number} {message[:4000]}")
    print(f"PARSED_LINES {parsed}")
    print(f"TOP_TYPES {dict(sorted(top_types.items()))}")
    print(f"PAYLOAD_TYPES {dict(sorted(payload_types.items()))}")
    print(f"FUNCTION_CALLS {len(calls)} OUTPUT_PAIRS {output_pairs}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
