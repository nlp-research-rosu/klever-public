#!/usr/bin/env python3
"""Bounded content summary of every required pipeline-v3 generation record."""

from __future__ import annotations

import collections
import hashlib
import json
import re
from pathlib import Path


GENERATION = Path("/generation")
TRACE = next((GENERATION / "codex-trace").rglob("*.jsonl"))


def compact(text: str, limit: int = 360) -> str:
    value = re.sub(r"\s+", " ", text).strip()
    return value if len(value) <= limit else value[:limit] + "…"


def main() -> None:
    print("PIPELINE JSON RECORDS")
    for path in [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        GENERATION / "invocation.json",
        GENERATION / "metrics.json",
        GENERATION / "runtime-metrics.json",
        GENERATION / "usage.json",
    ]:
        record = json.loads(path.read_text())
        print(
            f"{path}: keys={sorted(record)} "
            f"schema={record.get('schema_version')} "
            f"status={record.get('status')} stage={record.get('stage')}"
        )

    print("\nTEXT RECORD SUMMARIES")
    for path in [
        GENERATION / "prompt.txt",
        GENERATION / "codex-last.txt",
        GENERATION / "codex-output.log",
    ]:
        digest = hashlib.sha256()
        lines = 0
        key_lines: list[str] = []
        first = ""
        last = ""
        with path.open("rb") as stream:
            for raw in stream:
                lines += 1
                digest.update(raw)
                decoded = raw.decode("utf-8", errors="replace").rstrip()
                if lines == 1:
                    first = decoded
                last = decoded
                if re.search(
                    r"(kompile|kprove|krun|#Top|WarnStuckClaimState|"
                    r"cases=|RESULT:|VALIDATED|Gate [ABC])",
                    decoded,
                ):
                    key_lines.append(decoded)
        print(
            f"{path}: lines={lines} sha256={digest.hexdigest()} "
            f"first={compact(first)!r} last={compact(last)!r} "
            f"key_line_count={len(key_lines)}"
        )
        if path.name != "codex-output.log":
            for line in key_lines[:40]:
                print(f"  KEY {compact(line)}")
        else:
            for line in key_lines[-40:]:
                print(f"  TAIL_KEY {compact(line)}")

    print("\nSTRUCTURED TRACE")
    outer_types = collections.Counter()
    item_types = collections.Counter()
    tool_names = collections.Counter()
    tool_inputs: list[tuple[int, str, str]] = []
    final_messages: list[str] = []
    with TRACE.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            item = json.loads(line)
            outer_types[item.get("type")] += 1
            payload = item.get("payload", {})
            if item.get("type") == "response_item":
                item_type = payload.get("type")
                item_types[item_type] += 1
                if item_type in {"custom_tool_call", "function_call"}:
                    name = payload.get("name", "")
                    tool_names[name] += 1
                    tool_inputs.append(
                        (line_number, name, str(payload.get("input", "")))
                    )
                if (
                    item_type == "message"
                    and payload.get("role") == "assistant"
                    and payload.get("phase") == "final_answer"
                ):
                    final_messages.append(str(payload.get("content", "")))
    print(f"path={TRACE}")
    print(f"outer_types={dict(outer_types)}")
    print(f"response_item_types={dict(item_types)}")
    print(f"tool_names={dict(tool_names)}")
    print(f"tool_call_count={len(tool_inputs)}")
    for line_number, name, tool_input in tool_inputs:
        print(
            f"  TOOL line={line_number} name={name} "
            f"input_sha256={hashlib.sha256(tool_input.encode()).hexdigest()} "
            f"input={compact(tool_input)!r}"
        )
    print(f"final_message_count={len(final_messages)}")
    for message in final_messages:
        print(f"  FINAL {compact(message, 1000)}")


if __name__ == "__main__":
    main()
