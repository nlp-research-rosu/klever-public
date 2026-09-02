#!/usr/bin/env python3
"""Parse every structured generation event and scan every required text record."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path("/generation-evidence")
TRACE = next((ROOT / "codex-trace").rglob("*.jsonl"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    text_records = [
        ROOT / "codex-last.txt",
        ROOT / "codex-output.log",
        ROOT / "prompt.txt",
    ]
    for path in text_records:
        text = path.read_text(errors="replace")
        print(
            f"TEXT {path.name}: lines={len(text.splitlines())} bytes={len(text.encode())} "
            f"sha256={digest(path)} top_lines={sum(line == '#Top' for line in text.splitlines())} "
            f"warn_stuck_mentions={text.count('WarnStuckClaimState')}"
        )

    types = Counter()
    subtypes = Counter()
    calls = []
    output_statuses = []
    assistant_messages = 0
    line_count = 0
    for line_count, line in enumerate(TRACE.read_text().splitlines(), 1):
        record = json.loads(line)
        kind = record.get("type")
        payload = record.get("payload", {})
        subtype = payload.get("type")
        types[kind] += 1
        subtypes[(kind, subtype)] += 1
        if kind == "response_item" and subtype in {
            "function_call",
            "custom_tool_call",
        }:
            calls.append(
                (
                    line_count,
                    payload.get("name"),
                    payload.get("arguments") or payload.get("input") or "",
                )
            )
        if kind == "response_item" and subtype == "function_call_output":
            output = payload.get("output", "")
            matches = re.findall(r"(?:Process exited with code|exit_code[\"'= :]+)(\d+)", str(output))
            output_statuses.append((line_count, matches[-1] if matches else "not-recorded"))
        if (
            kind == "response_item"
            and subtype == "message"
            and payload.get("role") == "assistant"
        ):
            assistant_messages += 1

    print(
        f"TRACE {TRACE.relative_to(ROOT)}: lines={line_count} bytes={TRACE.stat().st_size} "
        f"sha256={digest(TRACE)} json_parse=PASS"
    )
    print(f"event_types={dict(types)}")
    print(f"event_subtypes={dict(subtypes)}")
    print(f"assistant_message_count={assistant_messages}")
    print(f"tool_call_count={len(calls)} tool_output_count={len(output_statuses)}")
    print("UNTRUSTED_TOOL_CALLS_BEGIN")
    for line, name, arguments in calls:
        compact = " ".join(str(arguments).split())
        if len(compact) > 1000:
            compact = compact[:1000] + "...[bounded]"
        print(f"trace_line={line} name={name} args={compact}")
    print("UNTRUSTED_TOOL_CALLS_END")
    print("OVERALL=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
