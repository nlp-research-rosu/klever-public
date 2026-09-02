#!/usr/bin/env python3
"""Summarize, without trusting, the candidate's generation records."""

from __future__ import annotations

import collections
import glob
import hashlib
import json
from pathlib import Path

CANDIDATE = Path("/candidate")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def show_text_record(name: str) -> None:
    path = CANDIDATE / name
    print(f"\n[{name}] bytes={path.stat().st_size} sha256={sha256(path)}")
    if path.suffix == ".json":
        print(json.dumps(json.loads(path.read_text()), indent=2, sort_keys=True))
    else:
        print(path.read_text(errors="replace").strip())


def main() -> None:
    for name in ("run-input.json", "metrics.json", "codex-last.txt"):
        show_text_record(name)

    output = CANDIDATE / "codex-output.log"
    output_text = output.read_text(errors="replace")
    print(
        f"\n[codex-output.log] bytes={output.stat().st_size} "
        f"lines={len(output_text.splitlines())} sha256={sha256(output)}"
    )
    needles = (
        "#Top",
        "WarnStuckClaimState",
        "EXPECTED FAILURE",
        "VALIDATED",
        "KPROVE_PASSED",
    )
    for needle in needles:
        print(f"{needle!r} occurrences={output_text.count(needle)}")
    print("last_nonempty_lines:")
    for line in [line for line in output_text.splitlines() if line.strip()][-12:]:
        print(line[:500])

    traces = sorted(glob.glob("/candidate/codex-trace/**/*.jsonl", recursive=True))
    print(f"\n[structured generation traces] count={len(traces)}")
    for trace_name in traces:
        path = Path(trace_name)
        outer = collections.Counter()
        payload = collections.Counter()
        tool_names = collections.Counter()
        final_messages: list[str] = []
        records = 0
        for raw in path.read_text(errors="replace").splitlines():
            record = json.loads(raw)
            records += 1
            outer[record.get("type")] += 1
            item = record.get("payload", {})
            payload[item.get("type")] += 1
            if item.get("type") in {"custom_tool_call", "function_call"}:
                tool_names[item.get("name")] += 1
            if record.get("type") == "event_msg" and item.get("type") in {
                "agent_message",
                "task_complete",
            }:
                message = item.get("message") or item.get("last_agent_message")
                if message:
                    final_messages.append(message)
        print(
            f"{path}: bytes={path.stat().st_size} records={records} "
            f"sha256={sha256(path)}"
        )
        print(f"outer_types={dict(outer)}")
        print(f"payload_types={dict(payload)}")
        print(f"tool_names={dict(tool_names)}")
        if final_messages:
            print("last_claimed_agent_message:")
            print(final_messages[-1])


if __name__ == "__main__":
    main()
