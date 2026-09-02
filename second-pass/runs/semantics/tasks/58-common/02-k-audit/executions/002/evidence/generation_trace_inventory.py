#!/usr/bin/env python3
"""Read every structured generation-trace line and inventory untrusted actions."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")


def compact(value, limit: int = 1200) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    text = text.replace("\r", "\\r")
    if len(text) <= limit:
        return text
    return text[:800] + f"\n...<{len(text) - 1200} bytes omitted>...\n" + text[-400:]


def main() -> None:
    top_counts: collections.Counter[str] = collections.Counter()
    response_counts: collections.Counter[str] = collections.Counter()
    event_counts: collections.Counter[str] = collections.Counter()
    total = 0
    for path in sorted(TRACE_ROOT.rglob("*.jsonl")):
        print(f"TRACE_FILE {path}")
        for line_number, line in enumerate(path.read_text().splitlines(), 1):
            event = json.loads(line)
            total += 1
            top_type = event.get("type", "<missing>")
            top_counts[top_type] += 1
            payload = event.get("payload", {})
            if top_type == "response_item":
                item_type = payload.get("type", "<missing>")
                response_counts[item_type] += 1
                if item_type == "function_call":
                    print(
                        f"LINE {line_number} FUNCTION_CALL "
                        f"name={payload.get('name')} args={compact(payload.get('arguments', ''))}"
                    )
                elif item_type == "function_call_output":
                    print(
                        f"LINE {line_number} FUNCTION_OUTPUT "
                        f"call_id={payload.get('call_id')} output={compact(payload.get('output', ''))}"
                    )
                elif item_type == "message" and payload.get("role") == "assistant":
                    print(f"LINE {line_number} ASSISTANT_MESSAGE {compact(payload.get('content', ''))}")
            elif top_type == "event_msg":
                event_type = payload.get("type", "<missing>")
                event_counts[event_type] += 1
                if event_type in {"agent_message", "task_complete"}:
                    print(f"LINE {line_number} EVENT_{event_type} {compact(payload)}")

    print(f"TOTAL_JSON_LINES {total}")
    print(f"TOP_LEVEL_COUNTS {dict(sorted(top_counts.items()))}")
    print(f"RESPONSE_ITEM_COUNTS {dict(sorted(response_counts.items()))}")
    print(f"EVENT_MSG_COUNTS {dict(sorted(event_counts.items()))}")


if __name__ == "__main__":
    main()
