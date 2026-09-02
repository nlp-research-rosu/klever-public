#!/usr/bin/env python3
"""Bounded summary of the complete untrusted generation JSONL trace."""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path


def bounded(value, limit: int = 1600) -> str:
    text = json.dumps(value, ensure_ascii=False) if not isinstance(value, str) else value
    text = text.replace("\r", "\\r").replace("\n", "\\n")
    if len(text) > limit:
        return text[:limit] + f"...<truncated {len(text) - limit} chars>"
    return text


def main() -> int:
    path = Path(sys.argv[1])
    outer_counts: collections.Counter[str] = collections.Counter()
    payload_counts: collections.Counter[str] = collections.Counter()
    tool_calls = []
    proof_mentions = []
    final_messages = []
    first_timestamp = None
    last_timestamp = None

    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            event = json.loads(line)
            timestamp = event.get("timestamp")
            first_timestamp = first_timestamp or timestamp
            last_timestamp = timestamp
            outer_counts[event.get("type", "<missing>")] += 1
            payload = event.get("payload") or {}
            payload_type = payload.get("type", "<missing>")
            payload_counts[payload_type] += 1

            if payload_type == "custom_tool_call":
                tool_calls.append(
                    {
                        "line": line_number,
                        "name": payload.get("name"),
                        "input": bounded(payload.get("input", "")),
                    }
                )

            candidate_text = payload.get("message") or payload.get("last_agent_message") or ""
            if isinstance(candidate_text, str) and (
                "#Top" in candidate_text
                or "kprove" in candidate_text
                or "RESULT:" in candidate_text
            ):
                proof_mentions.append(
                    {"line": line_number, "text": bounded(candidate_text)}
                )

            if event.get("type") == "response_item":
                if payload_type == "message" and payload.get("phase") == "final_answer":
                    final_messages.append(
                        {"line": line_number, "content": bounded(payload.get("content", ""))}
                    )
            if event.get("type") == "event_msg" and payload_type == "agent_message":
                if payload.get("phase") == "final_answer":
                    final_messages.append(
                        {"line": line_number, "message": bounded(payload.get("message", ""))}
                    )

    result = {
        "path": str(path),
        "line_count": sum(outer_counts.values()),
        "first_timestamp": first_timestamp,
        "last_timestamp": last_timestamp,
        "outer_type_counts": dict(sorted(outer_counts.items())),
        "payload_type_counts": dict(sorted(payload_counts.items())),
        "tool_calls": tool_calls,
        "proof_mentions": proof_mentions,
        "final_messages": final_messages,
        "trust": "untrusted generation claims only",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
