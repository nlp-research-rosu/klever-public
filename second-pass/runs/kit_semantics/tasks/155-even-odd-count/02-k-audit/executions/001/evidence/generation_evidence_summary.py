#!/usr/bin/env python3
"""Read and summarize all untrusted generation transcript records."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")
OUTPUT_LOG = Path("/generation-evidence/codex-output.log")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    trace_files = sorted(TRACE_ROOT.rglob("*"))
    trace_files = [path for path in trace_files if path.is_file()]
    print(f"trace_files={len(trace_files)}")
    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    tool_names: collections.Counter[str] = collections.Counter()
    command_count = 0
    parse_errors = 0
    total_lines = 0
    extracted_commands: list[str] = []
    final_messages: list[str] = []
    for path in trace_files:
        print(f"trace_file={path} sha256={sha256(path)}")
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                total_lines += 1
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as error:
                    parse_errors += 1
                    print(f"JSON_ERROR {path}:{line_number}: {error}")
                    continue
                top_types[str(record.get("type"))] += 1
                payload = record.get("payload")
                if not isinstance(payload, dict):
                    continue
                payload_type = str(payload.get("type"))
                payload_types[payload_type] += 1
                name = payload.get("name")
                if isinstance(name, str):
                    tool_names[name] += 1
                if payload_type in {"function_call", "custom_tool_call"}:
                    raw = payload.get("arguments", payload.get("input"))
                    if isinstance(raw, str):
                        try:
                            args = json.loads(raw)
                        except json.JSONDecodeError:
                            args = None
                        if isinstance(args, dict) and isinstance(
                            args.get("cmd"), str
                        ):
                            command_count += 1
                            extracted_commands.append(args["cmd"])
                if payload_type == "message":
                    content = payload.get("content")
                    if isinstance(content, list):
                        texts = [
                            item.get("text")
                            for item in content
                            if isinstance(item, dict)
                            and isinstance(item.get("text"), str)
                        ]
                        joined = "\n".join(texts)
                        if "RESULT:" in joined:
                            final_messages.append(joined)
    print(f"trace_total_lines={total_lines}")
    print(f"trace_parse_errors={parse_errors}")
    print(f"trace_top_types={dict(sorted(top_types.items()))}")
    print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
    print(f"trace_tool_names={dict(sorted(tool_names.items()))}")
    print(f"trace_shell_command_count={command_count}")
    for index, command in enumerate(extracted_commands, 1):
        print(f"TRACE_COMMAND_{index}: {command}")
    for index, message in enumerate(final_messages, 1):
        print(f"TRACE_FINAL_MESSAGE_{index}: {message}")

    patterns = (
        "#Top",
        "kprove",
        "kompile",
        "WarnStuckClaimState",
        "[Error]",
        "RESULT:",
        "VALIDATED",
    )
    counts = collections.Counter()
    first_lines: list[str] = []
    last_lines: collections.deque[str] = collections.deque(maxlen=30)
    output_lines = 0
    with OUTPUT_LOG.open(encoding="utf-8", errors="replace") as stream:
        for line in stream:
            output_lines += 1
            if len(first_lines) < 30:
                first_lines.append(line.rstrip("\n"))
            last_lines.append(line.rstrip("\n"))
            for pattern in patterns:
                counts[pattern] += line.count(pattern)
    print(
        f"codex_output_lines={output_lines} "
        f"bytes={OUTPUT_LOG.stat().st_size} sha256={sha256(OUTPUT_LOG)}"
    )
    print(f"codex_output_pattern_counts={dict(counts)}")
    print("CODEX_OUTPUT_FIRST_30_BEGIN")
    print("\n".join(first_lines))
    print("CODEX_OUTPUT_FIRST_30_END")
    print("CODEX_OUTPUT_LAST_30_BEGIN")
    print("\n".join(last_lines))
    print("CODEX_OUTPUT_LAST_30_END")
    print("GENERATION_EVIDENCE_READ=COMPLETE")


if __name__ == "__main__":
    main()
