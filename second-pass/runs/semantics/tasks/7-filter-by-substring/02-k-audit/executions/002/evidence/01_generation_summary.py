#!/usr/bin/env python3
"""Bounded full-record summary for the legacy-selected-stage1 evidence."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


json_records = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/usage.json"),
]
for path in json_records:
    value = json.loads(path.read_text())
    print(f"{path}: sha256={sha(path)} keys={sorted(value)}")
    selected = {
        key: value[key]
        for key in (
            "schema_version",
            "status",
            "stage",
            "result_marker",
            "record_layout",
            "semantics_mode",
            "legacy_import",
            "exit_code",
            "timeout_marker",
        )
        if key in value
    }
    print(f"  selected={selected}")

for path in [
    Path("/generation-evidence/prompt.txt"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
]:
    text = path.read_text(errors="replace")
    print(
        f"{path}: sha256={sha(path)} bytes={path.stat().st_size} "
        f"lines={len(text.splitlines())}"
    )
    print(
        "  markers="
        + repr(
            {
                "KPROVE_PASSED": text.count("KPROVE_PASSED"),
                "#Top": text.count("#Top"),
                "kprove": text.count("kprove"),
                "kompile": text.count("kompile"),
            }
        )
    )
    lines = text.splitlines()
    print(f"  first={lines[:3]!r}")
    print(f"  last={lines[-3:]!r}")

for path in sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl")):
    top = Counter()
    payload = Counter()
    tool_names = Counter()
    assistant_messages: list[str] = []
    parse_errors: list[tuple[int, str]] = []
    line_count = 0
    for line_count, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
        try:
            item = json.loads(line)
        except Exception as err:  # pragma: no cover - evidence diagnostic
            parse_errors.append((line_count, str(err)))
            continue
        top[item.get("type", "?")] += 1
        body = item.get("payload")
        if not isinstance(body, dict):
            continue
        payload[body.get("type", "?")] += 1
        if body.get("type") in {"function_call", "custom_tool_call"}:
            tool_names[body.get("name", "?")] += 1
        if body.get("type") == "message" and body.get("role") == "assistant":
            content = body.get("content", [])
            text_parts = [
                part.get("text", "")
                for part in content
                if isinstance(part, dict) and part.get("type") == "output_text"
            ]
            assistant_messages.append(" ".join(text_parts))
    print(
        f"{path}: sha256={sha(path)} bytes={path.stat().st_size} "
        f"lines={line_count} parse_errors={parse_errors}"
    )
    print(f"  top_types={dict(top)}")
    print(f"  payload_types={dict(payload)}")
    print(f"  tool_names={dict(tool_names)}")
    print(f"  assistant_message_count={len(assistant_messages)}")
    print(f"  final_assistant={assistant_messages[-1] if assistant_messages else None!r}")
