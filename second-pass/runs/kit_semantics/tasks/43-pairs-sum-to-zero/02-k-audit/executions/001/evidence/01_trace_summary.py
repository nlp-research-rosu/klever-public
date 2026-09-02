#!/usr/bin/env python3
"""Parse every JSONL event in the structured generation trace."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")


def walk(value: object):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def main() -> None:
    counts: collections.Counter[str] = collections.Counter()
    role_counts: collections.Counter[str] = collections.Counter()
    tool_names: collections.Counter[str] = collections.Counter()
    command_fragments: list[str] = []
    text_fragments: list[str] = []
    total = 0
    parse_errors = 0
    files = sorted(TRACE_ROOT.rglob("*.jsonl"))
    print(f"trace_files={len(files)}")
    for path in files:
        local = 0
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                local += 1
                total += 1
                try:
                    event = json.loads(line)
                except json.JSONDecodeError as error:
                    parse_errors += 1
                    print(f"PARSE_ERROR {path}:{line_number}: {error}")
                    continue
                if isinstance(event, dict):
                    counts[str(event.get("type", "<none>"))] += 1
                for node in walk(event):
                    role = node.get("role")
                    if isinstance(role, str):
                        role_counts[role] += 1
                    name = node.get("name")
                    if isinstance(name, str) and (
                        "tool" in str(node.get("type", "")).lower()
                        or name
                        in {
                            "exec_command",
                            "write_stdin",
                            "apply_patch",
                            "update_plan",
                        }
                    ):
                        tool_names[name] += 1
                    command = node.get("cmd")
                    if isinstance(command, str):
                        command_fragments.append(command)
                    text = node.get("text")
                    if isinstance(text, str) and any(
                        needle in text
                        for needle in (
                            "kprove",
                            "kompile",
                            "#Top",
                            "PROOF.md",
                            "VALIDATED",
                            "SOUND",
                            "FAIL",
                        )
                    ):
                        text_fragments.append(text)
        print(f"TRACE {path}: lines={local}")
    print(f"total_events={total} parse_errors={parse_errors}")
    print(f"event_types={dict(sorted(counts.items()))}")
    print(f"roles={dict(sorted(role_counts.items()))}")
    print(f"tool_names={dict(sorted(tool_names.items()))}")
    print(f"command_fragments={len(command_fragments)}")
    for index, command in enumerate(command_fragments, 1):
        compact = " ".join(command.split())
        print(f"COMMAND[{index}] {compact[:1000]}")
    print(f"selected_text_fragments={len(text_fragments)}")
    for index, fragment in enumerate(text_fragments, 1):
        compact = " ".join(fragment.split())
        print(f"TEXT[{index}] {compact[:2000]}")


if __name__ == "__main__":
    main()
