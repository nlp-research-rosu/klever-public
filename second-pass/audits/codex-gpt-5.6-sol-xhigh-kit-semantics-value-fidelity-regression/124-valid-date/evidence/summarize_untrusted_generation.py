#!/usr/bin/env python3
"""Bounded inventory of candidate-authored generation claims (never authority)."""

from __future__ import annotations

from collections import Counter
import glob
import hashlib
import json
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    candidate = Path("/candidate")
    for name in (
        "run-input.json",
        "metrics.json",
        "codex-last.txt",
        "codex-output.log",
    ):
        path = candidate / name
        print(
            f"artifact={path} bytes={path.stat().st_size} sha256={digest(path)}"
        )
    run_input = json.loads((candidate / "run-input.json").read_text())
    metrics = json.loads((candidate / "metrics.json").read_text())
    print(
        "run_input_claim="
        + json.dumps(
            {
                "problem_id": run_input.get("problem_id"),
                "condition": run_input.get("condition"),
                "input_hashes": run_input.get("inputs"),
            },
            sort_keys=True,
        )
    )
    print(
        "metrics_claim="
        + json.dumps(
            {
                "model": metrics.get("model"),
                "exit_code": metrics.get("exit_code"),
                "timed_out": metrics.get("timed_out"),
                "duration_s": metrics.get("duration_s"),
            },
            sort_keys=True,
        )
    )
    last = (candidate / "codex-last.txt").read_text(encoding="utf-8")
    print("codex_last_claim=" + " ".join(last.split()))
    output = (candidate / "codex-output.log").read_text(
        encoding="utf-8", errors="replace"
    )
    print(
        "codex_output_markers="
        f"#Top:{output.count('#Top')},"
        f"WarnStuckClaimState:{output.count('WarnStuckClaimState')},"
        f"VALIDATED:{output.count('VALIDATED')},"
        f"mismatches=0:{output.count('mismatches=0')}"
    )

    trace_files = sorted(
        Path(path)
        for path in glob.glob("/candidate/codex-trace/**/*.jsonl", recursive=True)
    )
    for trace_path in trace_files:
        outer_types: Counter[str] = Counter()
        payload_types: Counter[str] = Counter()
        assistant_messages: list[str] = []
        line_count = 0
        for line in trace_path.read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            line_count += 1
            outer_types[str(row.get("type"))] += 1
            payload = row.get("payload") or {}
            payload_types[str(payload.get("type"))] += 1
            if (
                row.get("type") == "response_item"
                and payload.get("type") == "message"
                and payload.get("role") == "assistant"
            ):
                for item in payload.get("content", []):
                    text = item.get("text")
                    if text:
                        assistant_messages.append(" ".join(text.split()))
        print(
            f"trace={trace_path} lines={line_count} sha256={digest(trace_path)}"
        )
        print(f"trace_outer_types={dict(sorted(outer_types.items()))}")
        print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
        for message in assistant_messages[-5:]:
            print(f"trace_assistant_claim={message[:1000]}")


if __name__ == "__main__":
    main()
