#!/usr/bin/env python3
"""Produce a bounded, reviewer-authored inventory of a Codex JSONL trace."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def compact(value: object, limit: int = 3000) -> str:
    rendered = json.dumps(value, ensure_ascii=False, sort_keys=True)
    if len(rendered) > limit:
        return rendered[:limit] + f"... <{len(rendered) - limit} chars omitted>"
    return rendered


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} TRACE.jsonl", file=sys.stderr)
        return 64
    path = Path(sys.argv[1])
    counts: dict[str, int] = {}
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            record_type = record.get("type", "<missing>")
            payload = record.get("payload", {})
            subtype = payload.get("type", "") if isinstance(payload, dict) else ""
            key = f"{record_type}:{subtype}"
            counts[key] = counts.get(key, 0) + 1

            if record_type == "session_meta":
                selected = {
                    key: payload.get(key)
                    for key in (
                        "session_id",
                        "cwd",
                        "cli_version",
                        "model_provider",
                    )
                }
                print(f"LINE {line_number} SESSION {compact(selected)}")
            elif record_type == "turn_context":
                selected = {
                    key: payload.get(key)
                    for key in ("cwd", "model", "effort", "summary")
                    if key in payload
                }
                print(f"LINE {line_number} CONTEXT {compact(selected)}")
            elif record_type == "response_item" and subtype == "function_call":
                selected = {
                    key: payload.get(key)
                    for key in ("name", "arguments", "call_id")
                }
                print(f"LINE {line_number} CALL {compact(selected, 12000)}")
            elif record_type == "response_item" and subtype == "function_call_output":
                selected = {
                    key: payload.get(key)
                    for key in ("call_id", "output")
                }
                print(f"LINE {line_number} OUTPUT {compact(selected, 12000)}")
            elif record_type == "event_msg" and subtype in {
                "agent_message",
                "task_complete",
            }:
                selected = {
                    key: payload.get(key)
                    for key in ("type", "phase", "message", "last_agent_message")
                    if key in payload
                }
                print(f"LINE {line_number} MESSAGE {compact(selected, 6000)}")
    print("EVENT_COUNTS")
    for key in sorted(counts):
        print(f"{key} {counts[key]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
