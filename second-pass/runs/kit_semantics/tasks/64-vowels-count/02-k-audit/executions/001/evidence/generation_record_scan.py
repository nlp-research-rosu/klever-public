#!/usr/bin/env python3
"""Bounded content scan of all large untrusted generation records."""

from __future__ import annotations

import collections
import json
from pathlib import Path


def main() -> None:
    output_path = Path("/generation-evidence/codex-output.log")
    raw = output_path.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    lines = text.splitlines()
    needles = [
        "RESULT:",
        "#Top",
        "kprove ",
        "kompile ",
        "WarnStuckClaimState",
        "VALIDATED",
        "apply_patch",
    ]
    print("codex_output_bytes=", len(raw), sep="")
    print("codex_output_lines=", len(lines), sep="")
    print("codex_output_nul_bytes=", raw.count(b"\0"), sep="")
    for needle in needles:
        print(f"codex_output_count[{needle!r}]={text.count(needle)}")
    print("codex_output_last_nonempty_lines:")
    for line in [line for line in lines if line.strip()][-12:]:
        print(line[:500])

    trace_root = Path("/generation-evidence/codex-trace")
    top_types = collections.Counter()
    payload_types = collections.Counter()
    call_names = collections.Counter()
    records = 0
    for path in sorted(trace_root.rglob("*.jsonl")):
        for line in path.read_text().splitlines():
            record = json.loads(line)
            records += 1
            top = record.get("type")
            top_types[str(top)] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_type = payload.get("type")
                payload_types[str(payload_type)] += 1
                if payload_type in {"function_call", "custom_tool_call"}:
                    call_names[str(payload.get("name"))] += 1
    print("trace_records=", records, sep="")
    print("trace_top_types=", dict(sorted(top_types.items())), sep="")
    print("trace_payload_types=", dict(sorted(payload_types.items())), sep="")
    print("trace_tool_names=", dict(sorted(call_names.items())), sep="")


if __name__ == "__main__":
    main()
