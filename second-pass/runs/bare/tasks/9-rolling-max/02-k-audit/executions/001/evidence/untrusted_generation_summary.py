#!/usr/bin/env python3
"""Bounded structural summary of untrusted candidate generation evidence."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


CANDIDATE = Path("/candidate")
TRACE = CANDIDATE / (
    "codex-trace/2026/07/22/"
    "rollout-2026-07-22T03-58-35-019f890c-5871-7860-bdf0-023104b89308.jsonl"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    for name in ("run-input.json", "metrics.json"):
        path = CANDIDATE / name
        print(f"{name}: sha256={digest(path)}")
        print(json.dumps(json.loads(path.read_text()), sort_keys=True))

    last = CANDIDATE / "codex-last.txt"
    print(f"codex-last.txt: sha256={digest(last)}")
    print(last.read_text().strip())

    event_types: collections.Counter[str] = collections.Counter()
    response_types: collections.Counter[str] = collections.Counter()
    trace_lines = 0
    final_messages: list[str] = []
    with TRACE.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            trace_lines = line_number
            event = json.loads(line)
            event_types[event.get("type", "<missing>")] += 1
            payload = event.get("payload", {})
            if event.get("type") == "response_item":
                response_types[payload.get("type", "<missing>")] += 1
            if (
                event.get("type") == "event_msg"
                and payload.get("type") == "agent_message"
                and payload.get("phase") == "final_answer"
            ):
                final_messages.append(payload.get("message", ""))
    print(
        f"trace: lines={trace_lines} sha256={digest(TRACE)} "
        f"event_types={dict(event_types)} response_types={dict(response_types)}"
    )
    print(f"trace final messages={final_messages!r}")

    output_log = CANDIDATE / "codex-output.log"
    text = output_log.read_text(encoding="utf-8", errors="replace")
    needles = (
        "#Top",
        "WarnStuckClaimState",
        "python differential checks: 8000 passed",
        "RESULT: KPROVE_PASSED",
    )
    print(
        f"codex-output.log: lines={text.count(chr(10))} "
        f"bytes={len(text.encode())} sha256={digest(output_log)}"
    )
    for needle in needles:
        print(f"codex-output occurrences {needle!r}: {text.count(needle)}")


if __name__ == "__main__":
    main()
