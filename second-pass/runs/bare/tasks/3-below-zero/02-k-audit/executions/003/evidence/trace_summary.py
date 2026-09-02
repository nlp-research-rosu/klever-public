#!/usr/bin/env python3
"""Parse every structured generation trace line and summarize untrusted claims."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")


def clipped(value: str, limit: int = 800) -> str:
    normalized = value.replace("\x00", "<NUL>")
    return normalized if len(normalized) <= limit else normalized[:limit] + "…"


def main() -> None:
    files = sorted(TRACE_ROOT.rglob("*.jsonl"))
    if not files:
        raise SystemExit("no JSONL trace files")
    top_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    commands: list[str] = []
    outputs: list[str] = []
    messages: list[tuple[str, str]] = []
    parsed = 0

    for path in files:
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                record = json.loads(line)
                parsed += 1
                top_types[str(record.get("type"))] += 1
                payload = record.get("payload", {})
                payload_type = str(payload.get("type"))
                payload_types[payload_type] += 1
                if payload_type in {"custom_tool_call", "function_call"}:
                    name = payload.get("name")
                    raw = payload.get("input", payload.get("arguments", ""))
                    commands.append(f"{name}: {clipped(str(raw), 1600)}")
                elif payload_type in {
                    "custom_tool_call_output",
                    "function_call_output",
                }:
                    outputs.append(clipped(str(payload), 1200))
                elif payload_type == "message":
                    role = str(payload.get("role"))
                    content = payload.get("content", [])
                    text_parts = [
                        str(item.get("text", ""))
                        for item in content
                        if isinstance(item, dict)
                    ]
                    messages.append((role, clipped("\n".join(text_parts), 1600)))
                elif payload_type == "agent_message":
                    messages.append(
                        ("assistant", clipped(str(payload.get("message", "")), 1600))
                    )

    print(f"trace_files={len(files)} parsed_json_lines={parsed}")
    print(f"top_level_types={dict(sorted(top_types.items()))}")
    print(f"payload_types={dict(sorted(payload_types.items()))}")
    print(f"tool_calls={len(commands)} tool_outputs={len(outputs)}")
    print("TOOL CALLS (bounded rendering; every record was parsed)")
    for index, command in enumerate(commands, 1):
        print(f"[{index}] {command}")
    print("MESSAGES (bounded rendering)")
    for index, (role, message) in enumerate(messages, 1):
        if role in {"assistant", "user"}:
            print(f"[{index}] role={role} {message}")
    proof_mentions = 0
    output_log = Path("/generation-evidence/codex-output.log")
    with output_log.open(encoding="utf-8", errors="replace") as stream:
        for line in stream:
            if any(
                marker in line
                for marker in ("kprove", "kompile", "krun", "#Top", "WarnStuck")
            ):
                proof_mentions += 1
    print(
        "codex-output.log: fully scanned "
        f"lines_with_build/proof markers={proof_mentions}"
    )
    print("TRACE_INSPECTION: PASS")


if __name__ == "__main__":
    main()
