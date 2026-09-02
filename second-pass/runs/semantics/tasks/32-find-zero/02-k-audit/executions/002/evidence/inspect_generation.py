#!/usr/bin/env python3
"""Consume the complete legacy generation trace/log and emit a bounded inventory."""

from __future__ import annotations

import collections
import hashlib
import json
import re
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")
OUTPUT_LOG = Path("/generation-evidence/codex-output.log")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compact(value: object, limit: int = 500) -> str:
    rendered = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return rendered if len(rendered) <= limit else rendered[:limit] + "…"


def main() -> int:
    trace_files = sorted(TRACE_ROOT.rglob("*"))
    trace_files = [path for path in trace_files if path.is_file()]
    print(f"trace files: {len(trace_files)}")
    event_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    tool_names: collections.Counter[str] = collections.Counter()
    json_errors: list[str] = []
    selected: list[str] = []
    total_records = 0

    for path in trace_files:
        print(f"TRACE {path.relative_to(TRACE_ROOT)} bytes={path.stat().st_size} sha256={sha256(path)}")
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                total_records += 1
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as error:
                    json_errors.append(f"{path}:{line_number}: {error}")
                    continue
                event_types[str(record.get("type", "<none>"))] += 1
                payload = record.get("payload")
                if isinstance(payload, dict):
                    payload_type = str(payload.get("type", "<none>"))
                    payload_types[payload_type] += 1
                    if payload_type in {
                        "function_call",
                        "function_call_output",
                        "custom_tool_call",
                        "custom_tool_call_output",
                    }:
                        name = str(payload.get("name", payload.get("call_id", "<none>")))
                        tool_names[name] += 1
                    if payload_type in {
                        "function_call",
                        "custom_tool_call",
                        "agent_message",
                    }:
                        text = compact(payload, 1200)
                        if re.search(
                            r"kompile|kprove|krun|apply_patch|spec\\.k|verification\\.k|solution\\.mpy|RESULT:",
                            text,
                            re.IGNORECASE,
                        ):
                            selected.append(f"{path.name}:{line_number}: {text}")

    print(f"total JSONL records consumed: {total_records}")
    print(f"JSON parse errors: {len(json_errors)}")
    for error in json_errors:
        print(f"ERROR {error}")
    print(f"top-level event types: {dict(sorted(event_types.items()))}")
    print(f"payload types: {dict(sorted(payload_types.items()))}")
    print(f"tool/call identifiers: {dict(tool_names.most_common())}")
    print("\nSelected trace records mentioning proof artifacts/tools:")
    for item in selected:
        print(item)

    raw = OUTPUT_LOG.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    lines = text.splitlines()
    print("\nComplete codex-output.log consumption:")
    print(f"bytes={len(raw)} lines={len(lines)} sha256={hashlib.sha256(raw).hexdigest()}")
    print(f"replacement characters={text.count(chr(0xfffd))}")
    patterns = [
        r"kompile[^\r\n]*",
        r"kprove[^\r\n]*",
        r"krun[^\r\n]*",
        r"RESULT:[^\r\n]*",
        r"WarnStuckClaimState[^\r\n]*",
        r"#Top[^\r\n]*",
    ]
    for pattern in patterns:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        print(f"pattern={pattern!r} matches={len(matches)}")
        for match in matches[:40]:
            print(f"  {match[:600]}")
        if len(matches) > 40:
            print(f"  … {len(matches) - 40} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
