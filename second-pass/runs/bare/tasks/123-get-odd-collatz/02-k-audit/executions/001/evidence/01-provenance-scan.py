#!/usr/bin/env python3
"""Read and index all untrusted provenance logs without accepting their claims."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


candidate = Path("/candidate")
trace_paths = sorted((candidate / "codex-trace").rglob("*.jsonl"))
print(f"structured_trace_files={len(trace_paths)}")

for path in trace_paths:
    raw = path.read_bytes()
    lines = raw.splitlines()
    outer_types: collections.Counter[str] = collections.Counter()
    event_types: collections.Counter[str] = collections.Counter()
    assistant_messages: list[str] = []
    tool_call_count = 0
    tool_output_count = 0
    top_output_count = 0
    error_output_count = 0
    for line_number, line in enumerate(lines, start=1):
        item = json.loads(line)
        outer_types[str(item.get("type"))] += 1
        payload = item.get("payload", {})
        if item.get("type") == "event_msg":
            event_types[str(payload.get("type"))] += 1
            if payload.get("type") == "agent_message":
                assistant_messages.append(str(payload.get("message", "")))
        if item.get("type") == "response_item":
            payload_type = payload.get("type")
            if payload_type in {"custom_tool_call", "function_call"}:
                tool_call_count += 1
            if payload_type == "function_call_output":
                tool_output_count += 1
                rendered = json.dumps(payload.get("output", ""))
                top_output_count += int("#Top" in rendered)
                error_output_count += int("[Error]" in rendered)
    print(f"TRACE={path}")
    print(f"bytes={len(raw)} lines={len(lines)} sha256={hashlib.sha256(raw).hexdigest()}")
    print(f"outer_types={dict(outer_types)}")
    print(f"event_types={dict(event_types)}")
    print(
        f"tool_calls={tool_call_count} tool_outputs={tool_output_count} "
        f"outputs_mentioning_top={top_output_count} "
        f"outputs_mentioning_error={error_output_count}"
    )
    for index, message in enumerate(assistant_messages, start=1):
        one_line = " ".join(message.split())
        print(f"assistant_message_{index}={one_line}")

for name in ("run-input.json", "metrics.json", "codex-last.txt", "codex-output.log"):
    path = candidate / name
    raw = path.read_bytes()
    print(
        f"FILE={path} bytes={len(raw)} lines={len(raw.splitlines())} "
        f"sha256={hashlib.sha256(raw).hexdigest()}"
    )
    if name.endswith(".json"):
        value = json.loads(raw)
        print("json=" + json.dumps(value, sort_keys=True, separators=(",", ":")))
    else:
        text = raw.decode(errors="replace")
        print(
            f"mentions_top={text.count('#Top')} mentions_kprove={text.count('kprove')} "
            f"mentions_error={text.count('[Error]')} "
            f"mentions_vacuity={text.lower().count('vacu')}"
        )
        if name == "codex-last.txt":
            print("content=" + " ".join(text.split()))
