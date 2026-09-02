#!/usr/bin/env python3
"""Bounded summary of all untrusted provenance claims and the JSONL trace."""

from __future__ import annotations

import collections
import glob
import json
from pathlib import Path


for name in ["run-input.json", "metrics.json"]:
    path = Path("/candidate") / name
    print(name, json.dumps(json.loads(path.read_text(encoding="utf-8")), sort_keys=True))

for name in ["codex-last.txt"]:
    path = Path("/candidate") / name
    print(f"{name} BEGIN")
    print(path.read_text(encoding="utf-8"), end="")
    print(f"{name} END")

log_path = Path("/candidate/codex-output.log")
log_lines = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
proof_lines = [
    (number, line)
    for number, line in enumerate(log_lines, 1)
    if any(
        needle in line
        for needle in [
            "#Top",
            "WarnStuckClaimState",
            "kprove spec.k",
            "RESULT: KPROVE_PASSED",
            "safe domain",
        ]
    )
]
print(
    "codex-output.log",
    json.dumps(
        {
            "bytes": log_path.stat().st_size,
            "lines": len(log_lines),
            "bounded_proof_claim_lines": proof_lines,
        },
        sort_keys=True,
    ),
)

for trace_name in glob.glob("/candidate/codex-trace/**/*.jsonl", recursive=True):
    counts: collections.Counter[str] = collections.Counter()
    parse_errors = []
    final_messages = []
    proof_tool_outputs = []
    with open(trace_name, encoding="utf-8") as stream:
        for number, line in enumerate(stream, 1):
            try:
                record = json.loads(line)
            except Exception as exc:
                parse_errors.append((number, str(exc)))
                continue
            counts[record.get("type", "<none>")] += 1
            payload = record.get("payload", {})
            if (
                record.get("type") == "event_msg"
                and payload.get("type") == "agent_message"
                and payload.get("phase") == "final_answer"
            ):
                final_messages.append((number, payload.get("message")))
            serialized = json.dumps(record, ensure_ascii=False)
            if "#Top" in serialized:
                proof_tool_outputs.append(
                    {
                        "line": number,
                        "record_type": record.get("type"),
                        "payload_type": payload.get("type"),
                        "contains_kprove": "kprove" in serialized,
                    }
                )
    print(
        "TRACE_SUMMARY "
        + json.dumps(
            {
                "path": trace_name,
                "record_counts": counts,
                "parse_errors": parse_errors,
                "records_containing_top": proof_tool_outputs,
                "final_messages": final_messages,
            },
            sort_keys=True,
        )
    )
