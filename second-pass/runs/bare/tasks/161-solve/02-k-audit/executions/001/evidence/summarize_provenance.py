#!/usr/bin/env python3
"""Read candidate generation records as untrusted data and emit a bounded summary."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


CANDIDATE = Path("/candidate")
TRACE = CANDIDATE / "codex-trace/2026/07/22/rollout-2026-07-22T08-01-45-019f89ea-f6f2-71c1-85b5-d5ec0f90f188.jsonl"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(65536), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    for name in ("run-input.json", "metrics.json"):
        path = CANDIDATE / name
        print(f"UNTRUSTED {name}:")
        print(json.dumps(json.loads(path.read_text()), indent=2, sort_keys=True))

    for name in ("codex-last.txt", "codex-output.log"):
        path = CANDIDATE / name
        text = path.read_text(errors="replace")
        lines = text.splitlines()
        print(
            f"UNTRUSTED {name}: bytes={path.stat().st_size} "
            f"lines={len(lines)} sha256={digest(path)}"
        )
        if name == "codex-last.txt":
            print(text.rstrip())
        else:
            selected = [
                f"{number}:{line}"
                for number, line in enumerate(lines, 1)
                if any(
                    marker in line.lower()
                    for marker in (
                        "kprove spec.k",
                        "printed `#top`",
                        "result: kprove_passed",
                        "warnstuck",
                        "[error]",
                    )
                )
            ]
            print("Selected claimed execution/status lines:")
            print("\n".join(selected[-80:]) or "(none)")

    type_counts: collections.Counter[str] = collections.Counter()
    payload_counts: collections.Counter[str] = collections.Counter()
    tool_calls: list[dict[str, object]] = []
    final_messages: list[str] = []
    with TRACE.open(errors="replace") as stream:
        for number, line in enumerate(stream, 1):
            record = json.loads(line)
            type_counts[str(record.get("type"))] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_counts[str(payload.get("type"))] += 1
                if payload.get("type") == "custom_tool_call":
                    tool_calls.append(
                        {
                            "line": number,
                            "name": payload.get("name"),
                            "input_sha256": hashlib.sha256(
                                str(payload.get("input", "")).encode()
                            ).hexdigest(),
                        }
                    )
                if payload.get("type") in {"agent_message", "task_complete"}:
                    message = payload.get("message") or payload.get("last_agent_message")
                    if isinstance(message, str):
                        final_messages.append(message)

    print(
        f"UNTRUSTED structured trace: bytes={TRACE.stat().st_size} "
        f"sha256={digest(TRACE)}"
    )
    print("record types:", json.dumps(type_counts, sort_keys=True))
    print("payload types:", json.dumps(payload_counts, sort_keys=True))
    print("tool calls (content represented by hashes):")
    print(json.dumps(tool_calls, indent=2, sort_keys=True))
    print("terminal claims:")
    for message in final_messages:
        print(message)


if __name__ == "__main__":
    main()
