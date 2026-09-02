#!/usr/bin/env python3
"""Read all untrusted generation logs and emit a bounded structural summary."""

from __future__ import annotations

import collections
import hashlib
import json
import pathlib
import re
import sys


def digest(path: pathlib.Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def summarize_json(path: pathlib.Path) -> None:
    with path.open(encoding="utf-8") as stream:
        value = json.load(stream)
    print(f"{path}: sha256={digest(path)}")
    print(json.dumps(value, indent=2, sort_keys=True))


def summarize_text(path: pathlib.Path) -> None:
    patterns = re.compile(
        r"#Top|WarnStuckClaimState|\\[Error\\]|RESULT:|kprove|kompile|krun"
    )
    count = 0
    matched = 0
    last_matches: collections.deque[tuple[int, str]] = collections.deque(maxlen=20)
    with path.open(encoding="utf-8", errors="replace") as stream:
        for count, line in enumerate(stream, 1):
            if patterns.search(line):
                matched += 1
                last_matches.append((count, line.rstrip()))
    print(
        f"{path}: sha256={digest(path)} lines={count} "
        f"interesting_lines={matched}"
    )
    print("last 20 interesting lines:")
    for line_number, line in last_matches:
        print(f"{line_number}:{line[:500]}")


def summarize_jsonl(path: pathlib.Path) -> None:
    outer_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    tool_names: collections.Counter[str] = collections.Counter()
    malformed: list[tuple[int, str]] = []
    final_messages: list[str] = []
    count = 0
    with path.open(encoding="utf-8", errors="replace") as stream:
        for count, line in enumerate(stream, 1):
            try:
                value = json.loads(line)
            except Exception as error:  # evidence parser must retain malformed records
                malformed.append((count, repr(error)))
                continue
            outer_types[str(value.get("type"))] += 1
            payload = value.get("payload")
            if isinstance(payload, dict):
                payload_types[str(payload.get("type"))] += 1
                if payload.get("type") == "custom_tool_call":
                    tool_names[str(payload.get("name"))] += 1
                if payload.get("type") in {"message", "agent_message"}:
                    text = payload.get("message")
                    if text is None:
                        content = payload.get("content", [])
                        if isinstance(content, list):
                            text = " ".join(
                                str(item.get("text", ""))
                                for item in content
                                if isinstance(item, dict)
                            )
                    if isinstance(text, str) and "RESULT:" in text:
                        final_messages.append(text[-800:])
    print(f"{path}: sha256={digest(path)} lines={count}")
    print(f"malformed={malformed}")
    print(f"outer_types={dict(sorted(outer_types.items()))}")
    print(f"payload_types={dict(sorted(payload_types.items()))}")
    print(f"tool_names={dict(sorted(tool_names.items()))}")
    print("records containing a final RESULT marker:")
    for message in final_messages:
        print(message.replace("\n", "\\n"))


def main() -> int:
    if len(sys.argv) != 5:
        raise SystemExit(
            "usage: trace_summary.py RUN_INPUT METRICS TEXT_LOG JSONL_TRACE"
        )
    summarize_json(pathlib.Path(sys.argv[1]))
    summarize_json(pathlib.Path(sys.argv[2]))
    summarize_text(pathlib.Path(sys.argv[3]))
    summarize_jsonl(pathlib.Path(sys.argv[4]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
