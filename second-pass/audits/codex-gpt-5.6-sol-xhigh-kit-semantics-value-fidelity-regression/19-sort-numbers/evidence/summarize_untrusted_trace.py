#!/usr/bin/env python3
"""Bounded structural summary of the untrusted generation JSONL trace."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path


KEYWORDS = re.compile(
    r"#Top|WarnStuckClaimState|EXPECTED_FAILURE|kprove|sortKeyVS|oracle|mutation",
    re.IGNORECASE,
)


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} TRACE.jsonl", file=sys.stderr)
        return 64

    top_counts: Counter[str] = Counter()
    payload_counts: Counter[str] = Counter()
    response_counts: Counter[str] = Counter()
    assistant_messages: list[tuple[int, int, str, str]] = []
    keyword_hits: list[tuple[int, str, str]] = []

    with Path(sys.argv[1]).open(encoding="utf-8") as trace:
        for line_number, line in enumerate(trace, 1):
            record = json.loads(line)
            top_counts[record.get("type", "NONE")] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_counts[payload.get("type", "NONE")] += 1
            if record.get("type") == "response_item" and isinstance(payload, dict):
                response_counts[payload.get("type", "NONE")] += 1
                if payload.get("type") == "message" and payload.get("role") == "assistant":
                    text = "\n".join(
                        str(item.get("text", ""))
                        for item in payload.get("content", [])
                        if isinstance(item, dict) and "text" in item
                    )
                    preview = re.sub(r"\s+", " ", text)[:300]
                    assistant_messages.append(
                        (
                            line_number,
                            len(text.encode()),
                            hashlib.sha256(text.encode()).hexdigest(),
                            preview,
                        )
                    )
            match = KEYWORDS.search(line)
            if match:
                left = max(match.start() - 100, 0)
                context = re.sub(r"\s+", " ", line[left : left + 400])
                keyword_hits.append((line_number, match.group(), context))

    print("TOP_LEVEL_TYPES")
    for name, count in sorted(top_counts.items()):
        print(f"{name}={count}")
    print("PAYLOAD_TYPES")
    for name, count in sorted(payload_counts.items()):
        print(f"{name}={count}")
    print("RESPONSE_ITEM_TYPES")
    for name, count in sorted(response_counts.items()):
        print(f"{name}={count}")
    print("ASSISTANT_MESSAGES line bytes sha256 preview")
    for row in assistant_messages:
        print("\t".join(map(str, row)))
    print("KEYWORD_HITS first_80 line keyword context")
    for row in keyword_hits[:80]:
        print("\t".join(map(str, row)))
    print(f"KEYWORD_HIT_COUNT={len(keyword_hits)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
