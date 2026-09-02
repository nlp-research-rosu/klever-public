#!/usr/bin/env python3
"""Bounded structural inspection of the untrusted Codex JSONL trace."""

from __future__ import annotations

import collections
import hashlib
import json
import pathlib
import sys


def clip(value: object, limit: int = 1200) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    text = text.replace("\x00", "\\0")
    return text if len(text) <= limit else text[:limit] + "...[clipped]"


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} TRACE.jsonl", file=sys.stderr)
        return 64

    path = pathlib.Path(sys.argv[1])
    raw = path.read_bytes()
    lines = raw.splitlines()
    outer: collections.Counter[str] = collections.Counter()
    payloads: collections.Counter[str] = collections.Counter()
    calls: list[tuple[int, str, object]] = []
    call_outputs: list[tuple[int, str]] = []
    custom_calls: list[tuple[int, str, object]] = []
    custom_outputs: list[tuple[int, str]] = []
    assistant_messages: list[tuple[int, str]] = []
    errors: list[tuple[int, str]] = []

    for number, line in enumerate(lines, 1):
        try:
            event = json.loads(line)
        except Exception as err:
            errors.append((number, f"JSON parse error: {err}"))
            continue
        outer[str(event.get("type"))] += 1
        payload = event.get("payload")
        if not isinstance(payload, dict):
            continue
        kind = str(payload.get("type"))
        payloads[kind] += 1
        if kind == "function_call":
            calls.append((number, str(payload.get("name")), payload.get("arguments")))
        elif kind == "function_call_output":
            call_outputs.append((number, clip(payload.get("output"), 600)))
        elif kind == "custom_tool_call":
            custom_calls.append((number, str(payload.get("name")), payload.get("input")))
        elif kind == "custom_tool_call_output":
            custom_outputs.append((number, clip(payload.get("output"), 1000)))
        elif kind == "message" and payload.get("role") == "assistant":
            content = payload.get("content")
            assistant_messages.append((number, clip(content, 1600)))
        elif kind in {"error", "turn_aborted"}:
            errors.append((number, clip(payload)))

    print(f"path={path}")
    print(f"bytes={len(raw)}")
    print(f"lines={len(lines)}")
    print(f"sha256={hashlib.sha256(raw).hexdigest()}")
    print("outer_types=" + json.dumps(dict(sorted(outer.items())), sort_keys=True))
    print("payload_types=" + json.dumps(dict(sorted(payloads.items())), sort_keys=True))
    print(f"function_calls={len(calls)}")
    for number, name, arguments in calls:
        print(f"CALL line={number} name={name} args={clip(arguments)}")
    print(f"function_call_outputs={len(call_outputs)}")
    for number, output in call_outputs:
        print(f"CALL_OUTPUT line={number} output={output}")
    print(f"custom_tool_calls={len(custom_calls)}")
    for number, name, call_input in custom_calls:
        print(f"CUSTOM_CALL line={number} name={name} input={clip(call_input, 1800)}")
    print(f"custom_tool_call_outputs={len(custom_outputs)}")
    for number, output in custom_outputs:
        print(f"CUSTOM_OUTPUT line={number} output={output}")
    print(f"assistant_messages={len(assistant_messages)}")
    for number, content in assistant_messages:
        print(f"ASSISTANT line={number} content={content}")
    print(f"errors={len(errors)}")
    for number, error in errors:
        print(f"ERROR line={number} content={error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
