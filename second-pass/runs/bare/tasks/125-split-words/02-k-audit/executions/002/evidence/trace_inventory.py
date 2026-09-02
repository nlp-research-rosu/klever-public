#!/usr/bin/env python3
"""Read every structured trace record and inventory its observable contents."""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")


def subtype(record: dict) -> str:
    payload = record.get("payload")
    if not isinstance(payload, dict):
        return "-"
    return str(payload.get("type", payload.get("name", "-")))


def main() -> None:
    print("COMMAND: python3 /audit-output/evidence/trace_inventory.py")
    files = sorted(TRACE_ROOT.rglob("*"))
    files = [path for path in files if path.is_file()]
    assert files, "structured trace has no files"
    counts: collections.Counter[tuple[str, str]] = collections.Counter()
    tool_counts: collections.Counter[str] = collections.Counter()
    shell_commands: list[tuple[int, str]] = []
    total = 0
    for path in files:
        with path.open() as stream:
            for line_number, line in enumerate(stream, 1):
                record = json.loads(line)
                total += 1
                record_type = str(record.get("type", "-"))
                counts[(record_type, subtype(record))] += 1
                payload = record.get("payload", {})
                if record_type == "response_item" and isinstance(payload, dict):
                    if payload.get("type") == "custom_tool_call":
                        name = str(payload.get("name", "-"))
                        tool_counts[name] += 1
                        tool_input = str(payload.get("input", ""))
                        for match in re.finditer(
                            r"(?:cmd|command):\\s*([\"'])(.*?)\\1",
                            tool_input,
                            flags=re.DOTALL,
                        ):
                            command = bytes(
                                match.group(2), "utf-8"
                            ).decode("unicode_escape")
                            shell_commands.append((line_number, command))
        print(f"READ {path}: {line_number} JSON records")
    print(f"TOTAL_RECORDS {total}")
    for (record_type, record_subtype), count in sorted(counts.items()):
        print(f"TYPE {record_type}/{record_subtype}: {count}")
    for name, count in sorted(tool_counts.items()):
        print(f"TOOL {name}: {count}")
    for line_number, command in shell_commands:
        first_line = command.splitlines()[0]
        print(f"SHELL line={line_number}: {first_line[:240]}")
    print("TRACE_INVENTORY: PASS")


if __name__ == "__main__":
    main()
