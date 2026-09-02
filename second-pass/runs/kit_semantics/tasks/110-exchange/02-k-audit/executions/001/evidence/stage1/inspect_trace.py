#!/usr/bin/env python3
"""Print a bounded semantic index of every event in the generation trace."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path("/generation-evidence/codex-trace")


def compact(value: object, limit: int = 1200) -> str:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    text = text.replace("\r", "\\r").replace("\n", "\\n")
    if len(text) > limit:
        return text[:limit] + f"...[truncated {len(text) - limit} chars]"
    return text


def main() -> None:
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        print(f"FILE {path.relative_to(ROOT)}")
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                item = json.loads(line)
                event_type = item.get("type")
                payload = item.get("payload")
                payload_type = (
                    payload.get("type") if isinstance(payload, dict) else None
                )
                if event_type in {"session_meta", "turn_context", "world_state"}:
                    print(
                        f"{line_number:04d} {event_type}/{payload_type}: "
                        f"{compact(payload)}"
                    )
                elif payload_type in {
                    "agent_message",
                    "message",
                    "user_message",
                    "task_started",
                    "task_complete",
                }:
                    print(
                        f"{line_number:04d} {event_type}/{payload_type}: "
                        f"{compact(payload, 3000)}"
                    )
                elif payload_type in {"function_call", "custom_tool_call"}:
                    print(
                        f"{line_number:04d} {event_type}/{payload_type}: "
                        f"{compact(payload, 5000)}"
                    )
                elif payload_type in {
                    "function_call_output",
                    "custom_tool_call_output",
                    "patch_apply_end",
                }:
                    print(
                        f"{line_number:04d} {event_type}/{payload_type}: "
                        f"{compact(payload, 1400)}"
                    )
                elif payload_type == "token_count":
                    print(
                        f"{line_number:04d} {event_type}/{payload_type}: "
                        f"{compact(payload)}"
                    )
                elif payload_type == "reasoning":
                    summary = payload.get("summary")
                    if summary:
                        print(
                            f"{line_number:04d} {event_type}/{payload_type}: "
                            f"{compact(summary, 1400)}"
                        )


if __name__ == "__main__":
    main()
