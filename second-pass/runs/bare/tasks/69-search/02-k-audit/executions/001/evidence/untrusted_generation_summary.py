#!/usr/bin/env python3
"""Bounded full-file summary of untrusted generator reports and trace."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


CANDIDATE = Path("/candidate")
TRACE = next((CANDIDATE / "codex-trace").rglob("*.jsonl"))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> None:
    print("UNTRUSTED METADATA")
    for name in ("run-input.json", "metrics.json"):
        path = CANDIDATE / name
        print(name, json.dumps(json.loads(path.read_text()), sort_keys=True))

    last_path = CANDIDATE / "codex-last.txt"
    print("codex-last.txt", json.dumps(last_path.read_text()))

    output_path = CANDIDATE / "codex-output.log"
    markers = ("#Top", "WarnStuckClaimState", "kprove ", "kompile ", "krun ")
    counts = collections.Counter()
    selected: collections.deque[str] = collections.deque(maxlen=30)
    output_lines = 0
    with output_path.open(encoding="utf-8", errors="replace") as stream:
        for output_lines, line in enumerate(stream, start=1):
            for marker in markers:
                if marker in line:
                    counts[marker] += 1
                    selected.append(line.rstrip()[:500])
    print(
        "codex-output.log",
        json.dumps(
            {
                "sha256": digest(output_path),
                "lines": output_lines,
                "marker_counts": counts,
                "last_marker_lines_bounded": list(selected),
            },
            sort_keys=True,
        ),
    )

    type_counts = collections.Counter()
    payload_type_counts = collections.Counter()
    final_messages: list[str] = []
    trace_lines = 0
    with TRACE.open(encoding="utf-8") as stream:
        for trace_lines, line in enumerate(stream, start=1):
            item = json.loads(line)
            type_counts[item.get("type")] += 1
            payload = item.get("payload", {})
            if isinstance(payload, dict):
                payload_type_counts[payload.get("type")] += 1
                if payload.get("type") == "agent_message" and payload.get("phase") == "final_answer":
                    final_messages.append(str(payload.get("message", ""))[:2000])
    print(
        "structured_trace",
        json.dumps(
            {
                "path": str(TRACE),
                "sha256": digest(TRACE),
                "lines": trace_lines,
                "top_level_types": {
                    "<none>" if key is None else key: value
                    for key, value in type_counts.items()
                },
                "payload_types": {
                    "<none>" if key is None else key: value
                    for key, value in payload_type_counts.items()
                },
                "final_messages": final_messages,
            },
            sort_keys=True,
        ),
    )


if __name__ == "__main__":
    main()
