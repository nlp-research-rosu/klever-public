#!/usr/bin/env python3
"""Bounded summary of claims in generation records; no claim is trusted."""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path


CANDIDATE = Path("/candidate")


def main() -> int:
    print("UNTRUSTED codex-last.txt")
    print((CANDIDATE / "codex-last.txt").read_text(encoding="utf-8").rstrip())

    output = (CANDIDATE / "codex-output.log").read_text(encoding="utf-8")
    print("\nUNTRUSTED codex-output.log bounded facts")
    print(f"bytes={len(output.encode('utf-8'))} lines={len(output.splitlines())}")
    print(f"top_token_occurrences={len(re.findall(r'#Top', output))}")
    kprove_count = len(re.findall(r"kprove spec\.k", output))
    print(f"kprove_command_occurrences={kprove_count}")
    final_markers = [
        line for line in output.splitlines() if line.startswith("RESULT:")
    ]
    print(f"final_result_markers={final_markers}")

    trace_paths = sorted((CANDIDATE / "codex-trace").rglob("*.jsonl"))
    for trace_path in trace_paths:
        counts: collections.Counter[tuple[str, str]] = collections.Counter()
        last_agent_message = None
        records = 0
        with trace_path.open("r", encoding="utf-8") as stream:
            for records, line in enumerate(stream, 1):
                record = json.loads(line)
                payload = record.get("payload", {})
                counts[(record.get("type", ""), payload.get("type", ""))] += 1
                if payload.get("type") == "task_complete":
                    last_agent_message = payload.get("last_agent_message")
        print(f"\nUNTRUSTED trace={trace_path}")
        print(f"records={records}")
        for key, count in sorted(counts.items()):
            print(f"event={key!r} count={count}")
        print("task_complete_claim:")
        print(last_agent_message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
