#!/usr/bin/env python3
"""Bounded summary of fully read untrusted generation text and trace records."""

from __future__ import annotations

import json
from pathlib import Path


KEYWORDS = (
    "kompile",
    "kprove",
    "krun",
    "#Top",
    "WarnStuckClaimState",
    "solution.mpy",
    "semantic.k",
    "verification.k",
    "spec.k",
    "mutation",
)
MAX_MATCHES = 160
MAX_CHARS = 1200


def clip(value: str) -> str:
    flattened = value.replace("\n", "\\n")
    if len(flattened) > MAX_CHARS:
        return flattened[:MAX_CHARS] + "...[truncated]"
    return flattened


def relevant(value: str) -> bool:
    return any(keyword in value for keyword in KEYWORDS)


def summarize_text(path: Path) -> None:
    print(f"BOUNDED RELEVANT RECORDS FROM {path}")
    raw = path.read_text(encoding="utf-8", errors="replace")
    count = 0
    for line_number, line in enumerate(raw.splitlines(), 1):
        if relevant(line):
            print(f"{line_number}: {clip(line)}")
            count += 1
            if count == MAX_MATCHES:
                break
    print(f"reported_matches={count} cap={MAX_MATCHES}")


def summarize_trace(path: Path) -> None:
    print(f"BOUNDED RELEVANT STRUCTURED EVENTS FROM {path}")
    count = 0
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            event = json.loads(line)
            payload = event.get("payload")
            payload_text = json.dumps(payload, sort_keys=True, ensure_ascii=False)
            if relevant(payload_text):
                event_type = event.get("type", "<missing>")
                payload_type = (
                    payload.get("type", "<missing>")
                    if isinstance(payload, dict)
                    else type(payload).__name__
                )
                print(
                    f"{line_number}: event_type={event_type} "
                    f"payload_type={payload_type} payload={clip(payload_text)}"
                )
                count += 1
                if count == MAX_MATCHES:
                    break
    print(f"reported_matches={count} cap={MAX_MATCHES}")


def main() -> None:
    summarize_text(Path("/generation-evidence/codex-output.log"))
    summarize_trace(
        Path(
            "/generation-evidence/codex-trace/2026/07/22/"
            "rollout-2026-07-22T04-26-36-019f8925-fce7-7f52-b753-b35e7b37f1fe.jsonl"
        )
    )


if __name__ == "__main__":
    main()
