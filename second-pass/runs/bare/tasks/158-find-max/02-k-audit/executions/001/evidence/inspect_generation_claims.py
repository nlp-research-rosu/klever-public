#!/usr/bin/env python3
"""Summarize untrusted generation records without treating them as authority."""

from __future__ import annotations

import collections
import json
from pathlib import Path


CANDIDATE = Path("/candidate")
TRACE = CANDIDATE / (
    "codex-trace/2026/07/22/"
    "rollout-2026-07-22T07-55-11-019f89e4-f694-7913-995d-aa11955108b3.jsonl"
)


def main() -> None:
    for name in ("run-input.json", "metrics.json"):
        data = json.loads((CANDIDATE / name).read_text(encoding="utf-8"))
        print(f"{name}: {json.dumps(data, sort_keys=True)}")

    print("codex-last.txt:")
    print((CANDIDATE / "codex-last.txt").read_text(encoding="utf-8").rstrip())

    log = (CANDIDATE / "codex-output.log").read_text(
        encoding="utf-8", errors="replace"
    )
    needles = ("#Top", "WarnStuckClaimState", "RESULT:", "4,680")
    for needle in needles:
        print(f"codex-output.log count {needle!r}: {log.count(needle)}")
    print("codex-output.log final 12 lines:")
    print("\n".join(log.splitlines()[-12:]))

    top_types: collections.Counter[str | None] = collections.Counter()
    payload_types: collections.Counter[str | None] = collections.Counter()
    record_count = 0
    final_messages: list[str] = []
    with TRACE.open(encoding="utf-8") as stream:
        for line in stream:
            record = json.loads(line)
            record_count += 1
            top_types[record.get("type")] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_types[payload.get("type")] += 1
                if (
                    payload.get("type") == "message"
                    and payload.get("role") == "assistant"
                    and payload.get("phase") == "final_answer"
                ):
                    for item in payload.get("content", []):
                        if item.get("type") == "output_text":
                            final_messages.append(item.get("text", ""))
    print(f"trace records: {record_count}")
    print(f"trace top-level types: {dict(top_types)}")
    print(f"trace payload types: {dict(payload_types)}")
    print("trace final assistant claim:")
    print("\n".join(final_messages))


if __name__ == "__main__":
    main()
