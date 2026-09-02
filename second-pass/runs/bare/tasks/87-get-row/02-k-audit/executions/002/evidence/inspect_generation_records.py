#!/usr/bin/env python3
"""Bounded inspection of the complete untrusted generation log and trace."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path


def short(text: str, limit: int = 260) -> str:
    return " ".join(text.split())[:limit]


def main() -> None:
    root = Path("/generation-evidence")
    output_bytes = (root / "codex-output.log").read_bytes()
    output = output_bytes.decode("utf-8", errors="replace")
    print(f"codex_output_bytes={len(output_bytes)}")
    print(f"codex_output_lines={len(output.splitlines())}")
    print(f"codex_output_sha256={hashlib.sha256(output_bytes).hexdigest()}")
    for marker in (
        "kompile",
        "krun",
        "kprove",
        "#Top",
        "KPROVE_PASSED",
        "1000 randomized CPython oracle checks",
    ):
        print(f"codex_output_occurrences[{marker!r}]={output.count(marker)}")
    print(f"codex_output_first={short(output.splitlines()[0])}")
    print(f"codex_output_last={short(output.splitlines()[-1])}")

    traces = sorted((root / "codex-trace").rglob("*.jsonl"))
    events = Counter()
    relevant_calls = []
    final_messages = []
    for trace in traces:
        with trace.open() as stream:
            for number, line in enumerate(stream, 1):
                event = json.loads(line)
                payload = event.get("payload", {})
                events[(event.get("type", "?"), payload.get("type", "-"))] += 1
                if (
                    event.get("type") == "response_item"
                    and payload.get("type") == "custom_tool_call"
                ):
                    call_input = payload.get("input", "")
                    if any(
                        marker in call_input
                        for marker in (
                            "kompile",
                            "krun",
                            "kprove",
                            "solution.py",
                            "semantic.k",
                            "verification.k",
                            "spec.k",
                            "prove.sh",
                        )
                    ):
                        relevant_calls.append(
                            (
                                number,
                                hashlib.sha256(call_input.encode()).hexdigest(),
                                short(call_input),
                            )
                        )
                if payload.get("type") == "agent_message" and payload.get("phase") == "final_answer":
                    final_messages.append(payload.get("message", ""))
    print(f"trace_files={len(traces)}")
    print(f"trace_json_events={sum(events.values())}")
    print(f"relevant_generation_calls={len(relevant_calls)}")
    for number, digest, preview in relevant_calls:
        print(f"  trace_line={number} input_sha256={digest} preview={preview}")
    print(f"final_messages={len(final_messages)}")
    for message in final_messages:
        print(f"  final={short(message, 600)}")


if __name__ == "__main__":
    main()
