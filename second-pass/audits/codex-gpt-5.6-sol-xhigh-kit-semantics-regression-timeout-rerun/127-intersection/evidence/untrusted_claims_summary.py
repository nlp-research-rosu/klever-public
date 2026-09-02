#!/usr/bin/env python3
"""Bounded summary of candidate generation claims; never executes candidate code."""

import collections
import hashlib
import json
import re
from pathlib import Path


CANDIDATE = Path("/candidate")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    named = [
        CANDIDATE / "run-input.json",
        CANDIDATE / "metrics.json",
        CANDIDATE / "codex-last.txt",
        CANDIDATE / "codex-output.log",
    ]
    trace_files = sorted((CANDIDATE / "codex-trace").rglob("*.jsonl"))
    for path in [*named, *trace_files]:
        print(
            f"ARTIFACT path={path} bytes={path.stat().st_size} "
            f"sha256={digest(path)}"
        )

    print("RUN_INPUT=" + json.dumps(
        json.loads((CANDIDATE / "run-input.json").read_text(encoding="utf-8")),
        sort_keys=True,
    ))
    print("METRICS=" + json.dumps(
        json.loads((CANDIDATE / "metrics.json").read_text(encoding="utf-8")),
        sort_keys=True,
    ))
    print("CODEX_LAST_BEGIN")
    print((CANDIDATE / "codex-last.txt").read_text(encoding="utf-8").rstrip())
    print("CODEX_LAST_END")

    pattern = re.compile(
        r"(#Top|WarnStuckClaimState|mismatches=|program_identity=|"
        r"KPROVE_PASSED|VALIDATED|kompile |kprove |krun )"
    )
    matches = []
    output_lines = 0
    with (CANDIDATE / "codex-output.log").open(
        encoding="utf-8", errors="replace"
    ) as stream:
        for line_number, line in enumerate(stream, 1):
            output_lines = line_number
            if pattern.search(line):
                matches.append((line_number, line.rstrip()))
    print(
        f"CODEX_OUTPUT lines={output_lines} selected_matches={len(matches)} "
        "showing_last=80"
    )
    for line_number, line in matches[-80:]:
        print(f"CODEX_OUTPUT_MATCH {line_number}: {line[:600]}")

    for trace_path in trace_files:
        counts = collections.Counter()
        tool_names = collections.Counter()
        malformed = 0
        final_messages = []
        lines = 0
        with trace_path.open(encoding="utf-8", errors="replace") as stream:
            for lines, line in enumerate(stream, 1):
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    malformed += 1
                    continue
                counts[event.get("type", "<missing>")] += 1
                payload = event.get("payload", {})
                if isinstance(payload, dict):
                    if payload.get("type") == "function_call":
                        tool_names[payload.get("name", "<missing>")] += 1
                    if payload.get("type") == "agent_message" and (
                        payload.get("phase") == "final_answer"
                    ):
                        final_messages.append(payload.get("message", ""))
        print(
            f"TRACE path={trace_path} lines={lines} malformed={malformed} "
            f"types={dict(sorted(counts.items()))} "
            f"tool_calls={dict(sorted(tool_names.items()))}"
        )
        for message in final_messages[-3:]:
            print("TRACE_FINAL=" + message.replace("\n", "\\n")[:2000])


if __name__ == "__main__":
    main()
