#!/usr/bin/env python3
"""Parse every generation trace line and inventory its human-visible records."""

from __future__ import annotations

import collections
import hashlib
import json
import re
import sys
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")
OUTPUT_LOG = Path("/generation-evidence/codex-output.log")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    trace_files = sorted(TRACE_ROOT.rglob("*.jsonl"))
    if not trace_files:
        print("ERROR: no structured trace files")
        return 1

    outer_types = collections.Counter()
    inner_types = collections.Counter()
    roles = collections.Counter()
    calls = []
    call_outputs = {}
    visible_messages = []
    parse_errors = []
    line_count = 0

    for trace_file in trace_files:
        with trace_file.open("r", encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, start=1):
                line_count += 1
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as err:
                    parse_errors.append((trace_file, line_number, str(err)))
                    continue
                outer_types[record.get("type", "<missing>")] += 1
                payload = record.get("payload")
                if not isinstance(payload, dict):
                    continue
                inner_type = payload.get("type", "<missing>")
                inner_types[inner_type] += 1
                if inner_type == "function_call":
                    calls.append(
                        (
                            trace_file.relative_to(TRACE_ROOT).as_posix(),
                            line_number,
                            payload.get("call_id") or payload.get("id"),
                            payload.get("name"),
                            payload.get("arguments"),
                        )
                    )
                elif inner_type == "function_call_output":
                    output = payload.get("output", "")
                    if not isinstance(output, str):
                        output = json.dumps(
                            output, sort_keys=True, separators=(",", ":")
                        )
                    call_outputs[payload.get("call_id")] = (
                        trace_file.relative_to(TRACE_ROOT).as_posix(),
                        line_number,
                        len(output),
                        hashlib.sha256(output.encode("utf-8")).hexdigest(),
                        output,
                    )
                elif inner_type == "message":
                    role = payload.get("role", "<missing>")
                    roles[role] += 1
                    texts = []
                    for item in payload.get("content", []):
                        if isinstance(item, dict):
                            text = item.get("text")
                            if isinstance(text, str):
                                texts.append(text)
                    if texts:
                        visible_messages.append(
                            (
                                trace_file.relative_to(TRACE_ROOT).as_posix(),
                                line_number,
                                role,
                                "\n".join(texts),
                            )
                        )
                elif inner_type == "agent_message":
                    message = payload.get("message")
                    if isinstance(message, str):
                        visible_messages.append(
                            (
                                trace_file.relative_to(TRACE_ROOT).as_posix(),
                                line_number,
                                "agent_message",
                                message,
                            )
                        )

    print(f"trace_files={len(trace_files)}")
    print(f"trace_lines={line_count}")
    print(f"parse_errors={len(parse_errors)}")
    for path in trace_files:
        print(
            f"TRACE_FILE path={path.relative_to(TRACE_ROOT).as_posix()} "
            f"bytes={path.stat().st_size} sha256={sha256(path)}"
        )
    for key, value in sorted(outer_types.items()):
        print(f"OUTER_TYPE {key} {value}")
    for key, value in sorted(inner_types.items()):
        print(f"INNER_TYPE {key} {value}")
    for key, value in sorted(roles.items()):
        print(f"MESSAGE_ROLE {key} {value}")

    print(f"function_calls={len(calls)}")
    for index, (path, line, call_id, name, arguments) in enumerate(calls, start=1):
        linked = call_outputs.get(call_id)
        if linked:
            _, output_line, output_length, output_hash, output = linked
            exit_match = re.search(r"Process exited with code (\\d+)", output)
            exit_text = exit_match.group(1) if exit_match else "not-recorded"
            first_output_line = next(
                (candidate for candidate in output.splitlines() if candidate.strip()),
                "",
            )
            first_output_line = first_output_line[:240]
            print(
                f"CALL {index} path={path}:{line} name={name} "
                f"call_id={call_id} arguments={arguments}"
            )
            print(
                f"CALL_OUTPUT {index} line={output_line} chars={output_length} "
                f"sha256={output_hash} exit={exit_text} first={first_output_line!r}"
            )
        else:
            print(
                f"CALL {index} path={path}:{line} name={name} "
                f"call_id={call_id} arguments={arguments}"
            )
            print(f"CALL_OUTPUT {index} MISSING")

    print(f"visible_messages={len(visible_messages)}")
    for index, (path, line, role, text) in enumerate(visible_messages, start=1):
        print(
            f"MESSAGE {index} path={path}:{line} role={role} chars={len(text)} "
            f"sha256={hashlib.sha256(text.encode('utf-8')).hexdigest()}"
        )
        if role in {"assistant", "agent_message"}:
            print(text)

    print(
        f"OUTPUT_LOG bytes={OUTPUT_LOG.stat().st_size} "
        f"sha256={sha256(OUTPUT_LOG)}"
    )
    with OUTPUT_LOG.open("r", encoding="utf-8", errors="strict") as stream:
        output_lines = sum(1 for _ in stream)
    print(f"OUTPUT_LOG lines={output_lines} utf8=valid")

    for path, line, error in parse_errors:
        print(f"PARSE_ERROR {path}:{line}: {error}")
    return 1 if parse_errors else 0


if __name__ == "__main__":
    sys.exit(main())
