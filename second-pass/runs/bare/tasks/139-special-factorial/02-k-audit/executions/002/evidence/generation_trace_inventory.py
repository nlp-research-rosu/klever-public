#!/usr/bin/env python3
"""Read and inventory the complete untrusted generation transcript."""

from __future__ import annotations

import collections
import hashlib
import json
import re
import sys
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")
OUTPUT_LOG = Path("/generation-evidence/codex-output.log")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def shorten(text: str, limit: int = 360) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= limit else text[: limit - 3] + "..."


def main() -> int:
    trace_files = sorted(TRACE_ROOT.rglob("*.jsonl"))
    print(f"trace_files={len(trace_files)}")
    total_lines = 0
    outer_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    tool_names: collections.Counter[str] = collections.Counter()
    custom_call_ids: set[str] = set()
    custom_output_ids: set[str] = set()
    function_call_ids: set[str] = set()
    function_output_ids: set[str] = set()
    commands: list[tuple[int, str]] = []
    final_messages: list[str] = []

    for trace_file in trace_files:
        relative = trace_file.relative_to(TRACE_ROOT)
        print(
            f"TRACE_FILE {relative} size={trace_file.stat().st_size} "
            f"sha256={digest(trace_file)}"
        )
        with trace_file.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                total_lines += 1
                try:
                    event = json.loads(line)
                except json.JSONDecodeError as error:
                    print(f"INVALID_JSON {relative}:{line_number}: {error}")
                    return 1
                outer_types[str(event.get("type"))] += 1
                payload = event.get("payload") or {}
                payload_type = str(payload.get("type"))
                payload_types[payload_type] += 1

                if payload_type == "custom_tool_call":
                    call_id = str(payload.get("call_id"))
                    custom_call_ids.add(call_id)
                    name = str(payload.get("name"))
                    tool_names[name] += 1
                    call_input = str(payload.get("input") or "")
                    for match in re.finditer(
                        r'exec_command\(\{cmd:"((?:[^"\\]|\\.)*)"',
                        call_input,
                    ):
                        try:
                            command = json.loads('"' + match.group(1) + '"')
                        except json.JSONDecodeError:
                            command = match.group(1)
                        commands.append((line_number, shorten(command, 520)))
                elif payload_type == "custom_tool_call_output":
                    custom_output_ids.add(str(payload.get("call_id")))
                elif payload_type == "function_call":
                    function_call_ids.add(str(payload.get("call_id")))
                    tool_names[str(payload.get("name"))] += 1
                elif payload_type == "function_call_output":
                    function_output_ids.add(str(payload.get("call_id")))
                elif payload_type == "agent_message":
                    message = str(payload.get("message") or "")
                    if message:
                        final_messages.append(message)
                elif payload_type == "message" and payload.get("role") == "assistant":
                    content = payload.get("content") or []
                    message = " ".join(
                        str(block.get("text") or "")
                        for block in content
                        if isinstance(block, dict)
                    )
                    if message:
                        final_messages.append(message)

    print(f"trace_json_lines={total_lines}")
    print(f"outer_types={dict(sorted(outer_types.items()))}")
    print(f"payload_types={dict(sorted(payload_types.items()))}")
    print(f"tool_names={dict(sorted(tool_names.items()))}")
    print(
        "custom_call_output_pairing="
        f"{custom_call_ids == custom_output_ids} "
        f"calls={len(custom_call_ids)} outputs={len(custom_output_ids)}"
    )
    print(
        "function_call_output_pairing="
        f"{function_call_ids == function_output_ids} "
        f"calls={len(function_call_ids)} outputs={len(function_output_ids)}"
    )
    print(f"extracted_exec_commands={len(commands)}")
    for line_number, command in commands:
        print(f"  trace-line-{line_number}: {command}")
    print(f"assistant_messages={len(final_messages)}")
    for index, message in enumerate(final_messages, 1):
        print(f"  assistant-{index}: {shorten(message, 700)}")

    raw = OUTPUT_LOG.read_bytes()
    text = raw.decode("utf-8")
    print(
        f"CODEX_OUTPUT bytes={len(raw)} lines={len(text.splitlines())} "
        f"sha256={digest(OUTPUT_LOG)} nul_bytes={raw.count(bytes([0]))}"
    )
    for needle in (
        "#Top",
        "WarnStuckClaimState",
        "kompile",
        "kprove",
        "krun",
        "RESULT: KPROVE_PASSED",
    ):
        print(f"  occurrences {needle!r}: {text.count(needle)}")
    print(f"  first_line={shorten(text.splitlines()[0])}")
    print(f"  last_line={shorten(text.splitlines()[-1])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
