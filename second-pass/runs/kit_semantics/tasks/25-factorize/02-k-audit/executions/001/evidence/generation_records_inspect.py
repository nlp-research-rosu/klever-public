#!/usr/bin/env python3
"""Parse every pipeline-v3 generation record without treating it as authority."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


ROOT = Path("/generation-evidence")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def main() -> None:
    json_records = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        ROOT / "invocation.json",
        ROOT / "metrics.json",
        ROOT / "runtime-metrics.json",
        ROOT / "usage.json",
    ]
    text_records = [
        ROOT / "codex-last.txt",
        ROOT / "codex-output.log",
        ROOT / "prompt.txt",
    ]
    for path in json_records:
        raw = path.read_bytes()
        value = json.loads(raw)
        print(
            f"json_record={path} bytes={len(raw)} sha256={digest(raw)} "
            f"keys={sorted(value)}"
        )
    for path in text_records:
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        print(
            f"text_record={path} bytes={len(raw)} lines={len(text.splitlines())} "
            f"sha256={digest(raw)} utf8=true"
        )
        if path.name == "codex-output.log":
            needles = [
                "#Top",
                "WarnStuckClaimState",
                "EXPECTED FAILURE",
                "differential inputs=",
                "ERROR:",
                "timed out",
                "Killed",
            ]
            for needle in needles:
                print(f"codex_output_count[{needle!r}]={text.count(needle)}")

    trace_paths = sorted((ROOT / "codex-trace").rglob("*"))
    trace_files = [path for path in trace_paths if path.is_file()]
    print(f"trace_file_count={len(trace_files)}")
    for path in trace_files:
        raw = path.read_bytes()
        lines = raw.splitlines()
        type_counts: collections.Counter[str] = collections.Counter()
        payload_type_counts: collections.Counter[str] = collections.Counter()
        commands: list[str] = []
        final_messages: list[str] = []
        for number, line in enumerate(lines, start=1):
            event = json.loads(line)
            type_counts[str(event.get("type"))] += 1
            payload = event.get("payload")
            if isinstance(payload, dict):
                payload_type_counts[str(payload.get("type"))] += 1
                if payload.get("type") == "function_call":
                    name = payload.get("name")
                    arguments = payload.get("arguments")
                    commands.append(f"line={number} function={name} arguments={arguments}")
                if payload.get("type") == "custom_tool_call":
                    name = payload.get("name")
                    tool_input = payload.get("input")
                    commands.append(
                        f"line={number} custom_tool={name} input={tool_input}"
                    )
                if payload.get("type") == "message" and payload.get("role") == "assistant":
                    content = payload.get("content")
                    if isinstance(content, list):
                        for item in content:
                            if isinstance(item, dict) and item.get("type") in {
                                "output_text",
                                "text",
                            }:
                                text = item.get("text")
                                if isinstance(text, str) and "RESULT:" in text:
                                    final_messages.append(f"line={number} {text}")
        print(
            f"trace={path} bytes={len(raw)} lines={len(lines)} sha256={digest(raw)} "
            f"top_types={dict(type_counts)} payload_types={dict(payload_type_counts)}"
        )
        print(f"trace_function_call_count={len(commands)}")
        for command in commands:
            print(f"trace_function_call={command}")
        print(f"trace_final_message_count={len(final_messages)}")
        for message in final_messages:
            print(f"trace_final_message={message}")


if __name__ == "__main__":
    main()
