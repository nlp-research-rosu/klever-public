#!/usr/bin/env python3
"""Bounded inspection summary of the untrusted generation records."""

from __future__ import annotations

import glob
import json
from pathlib import Path


for path in (
    "/run.json",
    "/task.json",
    "/generation-result.json",
    "/generation-evidence/invocation.json",
    "/generation-evidence/metrics.json",
    "/generation-evidence/usage.json",
):
    doc = json.loads(Path(path).read_text())
    interesting = {
        key: doc[key]
        for key in (
            "schema_version",
            "record_layout",
            "problem_id",
            "stage",
            "status",
            "result_marker",
            "exit_code",
            "duration_s",
            "legacy_import",
            "condition",
            "inputs",
            "outputs",
        )
        if key in doc
    }
    print(f"RECORD {path}")
    print(json.dumps(interesting, indent=2, sort_keys=True))

print("TRACE SUMMARY")
for path in glob.glob("/generation-evidence/codex-trace/**/*.jsonl", recursive=True):
    for line_number, line in enumerate(Path(path).read_text().splitlines(), 1):
        event = json.loads(line)
        payload = event.get("payload", {})
        if event.get("type") == "response_item" and payload.get("type") == "custom_tool_call":
            raw = str(payload.get("input", "")).replace("\n", " ")
            print(
                f"line={line_number} tool={payload.get('name')} "
                f"input_prefix={raw[:500]}"
            )
        if (
            event.get("type") == "response_item"
            and payload.get("type") == "message"
            and payload.get("role") == "assistant"
        ):
            text = " ".join(
                item.get("text", "")
                for item in payload.get("content", [])
                if isinstance(item, dict)
            ).replace("\n", " ")
            print(f"line={line_number} assistant_prefix={text[:500]}")
        if event.get("type") == "event_msg" and payload.get("type") == "task_complete":
            print(
                f"line={line_number} task_complete "
                f"duration_ms={payload.get('duration_ms')}"
            )

output_log = Path("/generation-evidence/codex-output.log").read_text(errors="replace")
needles = (
    "#Top",
    "WarnStuckClaimState",
    "KPROVE_PASSED",
    "kprove spec.k",
    "kompile verification.k",
)
print("CODEX OUTPUT MATCH COUNTS")
for needle in needles:
    print(f"{needle!r}: {output_log.count(needle)}")

last = Path("/generation-evidence/codex-last.txt").read_text(errors="replace")
print("CODEX LAST")
print(last)
