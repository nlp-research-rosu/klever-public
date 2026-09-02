#!/usr/bin/env python3
"""Read every structured trace record and emit a bounded audit summary."""

from __future__ import annotations

import collections
import json
from pathlib import Path


ROOT = Path("/generation-evidence/codex-trace")


def text_blocks(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    blocks = []
    for item in value:
        if isinstance(item, dict):
            text = item.get("text")
            if isinstance(text, str):
                blocks.append(text)
    return blocks


def main() -> None:
    counts: collections.Counter[str] = collections.Counter()
    parsed = 0
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        print(f"TRACE_FILE {path.relative_to(ROOT)}")
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                record = json.loads(line)
                parsed += 1
                outer_type = str(record.get("type"))
                counts[outer_type] += 1
                payload = record.get("payload")
                if not isinstance(payload, dict):
                    continue
                payload_type = payload.get("type")
                if isinstance(payload_type, str):
                    counts[f"payload:{payload_type}"] += 1
                if outer_type == "response_item":
                    if payload_type == "custom_tool_call":
                        name = payload.get("name")
                        raw_input = payload.get("input", "")
                        print(
                            f"L{line_number} TOOL {name} "
                            f"{str(raw_input)[:1200]!r}"
                        )
                    elif payload_type == "custom_tool_call_output":
                        raw = " ".join(text_blocks(payload.get("output")))
                        if any(
                            token in raw
                            for token in (
                                "#Top",
                                "[Error]",
                                "exit_code",
                                "Script completed",
                            )
                        ):
                            print(f"L{line_number} TOOL_OUTPUT {raw[:1600]!r}")
                    elif payload_type == "message":
                        role = payload.get("role")
                        if role == "assistant":
                            raw = " ".join(text_blocks(payload.get("content")))
                            print(
                                f"L{line_number} ASSISTANT {raw[:1600]!r}"
                            )
                elif outer_type == "event_msg":
                    if payload_type in (
                        "task_started",
                        "task_complete",
                        "agent_message",
                    ):
                        print(
                            f"L{line_number} EVENT {payload_type} "
                            f"{str(payload)[:1600]!r}"
                        )
    print(f"PARSED_RECORDS {parsed}")
    for key, value in sorted(counts.items()):
        print(f"COUNT {key} {value}")


if __name__ == "__main__":
    main()
