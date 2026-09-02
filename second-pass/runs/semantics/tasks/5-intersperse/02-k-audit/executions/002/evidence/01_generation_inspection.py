#!/usr/bin/env python3
"""Read and summarize every required legacy-selected-stage1 generation record."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


root = Path("/generation-evidence")
records = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    root / "invocation.json",
    root / "metrics.json",
    root / "usage.json",
]

for path in records:
    data = json.loads(path.read_text(encoding="utf-8"))
    print(f"JSON_RECORD {path} sha256={hashlib.sha256(path.read_bytes()).hexdigest()}")
    print(json.dumps(data, sort_keys=True, separators=(",", ":")))

for name in ["codex-last.txt", "codex-output.log", "prompt.txt"]:
    path = root / name
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    print(
        f"TEXT_RECORD {path} bytes={len(raw)} lines={len(text.splitlines())} "
        f"sha256={hashlib.sha256(raw).hexdigest()}"
    )
    if name != "codex-output.log":
        print(text)
    else:
        selected = [
            f"{line_number}:{line}"
            for line_number, line in enumerate(text.splitlines(), 1)
            if any(
                token in line
                for token in (
                    "kompile",
                    "kprove",
                    "krun",
                    "#Top",
                    "[Error]",
                    "WarnStuck",
                    "RESULT:",
                )
            )
        ]
        print(f"selected_material_lines={len(selected)}")
        for line in selected:
            print(line[:1600])

trace_files = sorted((root / "codex-trace").rglob("*.jsonl"))
print(f"TRACE_FILE_COUNT {len(trace_files)}")
for path in trace_files:
    raw = path.read_bytes()
    events = [
        json.loads(line)
        for line in raw.decode("utf-8").splitlines()
        if line.strip()
    ]
    outer = collections.Counter(event.get("type") for event in events)
    payload_types = collections.Counter(
        event.get("payload", {}).get("type")
        for event in events
        if isinstance(event.get("payload"), dict)
    )
    print(
        f"TRACE {path} bytes={len(raw)} events={len(events)} "
        f"sha256={hashlib.sha256(raw).hexdigest()}"
    )
    print(f"outer_types={dict(sorted(outer.items()))}")
    print(f"payload_types={dict(sorted(payload_types.items(), key=lambda x: str(x[0])))}")
    call_index = 0
    for line_number, event in enumerate(events, 1):
        payload = event.get("payload", {})
        if event.get("type") != "response_item" or not isinstance(payload, dict):
            continue
        if payload.get("type") == "custom_tool_call":
            call_index += 1
            compact_input = " ".join(str(payload.get("input", "")).split())
            print(
                f"TRACE_CALL {call_index} line={line_number} "
                f"name={payload.get('name')} input={compact_input[:2400]}"
            )
        elif payload.get("type") == "custom_tool_call_output":
            content = payload.get("output", [])
            compact = " ".join(
                block.get("text", "")
                for block in content
                if isinstance(block, dict)
            )
            compact = " ".join(compact.split())
            print(f"TRACE_OUTPUT line={line_number} text={compact[:1200]}")
        elif payload.get("type") == "message" and payload.get("role") == "assistant":
            content = payload.get("content", [])
            compact = " ".join(
                block.get("text", "")
                for block in content
                if isinstance(block, dict)
            )
            compact = " ".join(compact.split())
            print(f"TRACE_ASSISTANT line={line_number} text={compact[:1600]}")
