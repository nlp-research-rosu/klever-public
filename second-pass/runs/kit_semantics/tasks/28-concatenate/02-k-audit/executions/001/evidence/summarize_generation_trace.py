#!/usr/bin/env python3
"""Bounded structural summary of every event in the untrusted generation JSONL."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path("/generation-evidence/codex-trace")


def compact(value: object, limit: int = 360) -> str:
    text = json.dumps(value, ensure_ascii=True, sort_keys=True)
    text = " ".join(text.split())
    return text if len(text) <= limit else text[:limit] + "...<bounded>"


def main() -> int:
    counts: Counter[str] = Counter()
    selected: list[str] = []
    for path in sorted(ROOT.rglob("*.jsonl")):
        with path.open() as stream:
            for line_number, line in enumerate(stream, 1):
                event = json.loads(line)
                event_type = event.get("type", "<missing>")
                payload = event.get("payload")
                payload_type = payload.get("type", "<missing>") if isinstance(payload, dict) else "<non-object>"
                counts[f"{event_type}/{payload_type}"] += 1
                if payload_type in {
                    "function_call",
                    "custom_tool_call",
                    "patch_apply_end",
                    "agent_message",
                    "task_complete",
                }:
                    selected.append(
                        f"{path.relative_to(ROOT)}:{line_number} "
                        f"{event_type}/{payload_type} {compact(payload)}"
                    )
    print(f"events={sum(counts.values())}")
    print(f"event_shapes={dict(sorted(counts.items()))}")
    print(f"selected_events={len(selected)}")
    for item in selected:
        print(item)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
