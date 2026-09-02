#!/usr/bin/env python3
"""Summarize candidate provenance files strictly as untrusted claims."""

from __future__ import annotations

import collections
import json
from pathlib import Path


ROOT = Path("/candidate")


def print_file(name: str):
    text = (ROOT / name).read_text(encoding="utf-8", errors="replace")
    print(f"===== UNTRUSTED {name} ({len(text.encode('utf-8'))} bytes) =====")
    print(text.rstrip())


def main() -> int:
    for name in ("run-input.json", "metrics.json", "codex-last.txt"):
        print_file(name)

    log = (ROOT / "codex-output.log").read_text(encoding="utf-8", errors="replace")
    print(f"===== UNTRUSTED codex-output.log ({len(log.encode('utf-8'))} bytes) =====")
    selected = [
        (line_number, line)
        for line_number, line in enumerate(log.splitlines(), 1)
        if any(
            marker in line
            for marker in (
                "#Top",
                "randomized CPython",
                "RESULT:",
                "returned(tupleVal",
                "exited 0",
                "Warning",
                "[Error]",
            )
        )
    ]
    for line_number, line in selected:
        print(f"{line_number}: {line}")

    traces = sorted((ROOT / "codex-trace").rglob("*.jsonl"))
    print(f"===== UNTRUSTED structured traces count={len(traces)} =====")
    for trace in traces:
        counts: collections.Counter[tuple[object, object]] = collections.Counter()
        agent_messages = []
        for line_number, line in enumerate(trace.read_text(encoding="utf-8").splitlines(), 1):
            event = json.loads(line)
            payload = event.get("payload") or {}
            counts[(event.get("type"), payload.get("type"))] += 1
            if payload.get("type") == "agent_message":
                agent_messages.append((line_number, payload.get("message", "")))
        print(f"trace={trace} event_counts={dict(counts)}")
        for line_number, message in agent_messages:
            print(f"trace_line={line_number} agent_claim={message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
