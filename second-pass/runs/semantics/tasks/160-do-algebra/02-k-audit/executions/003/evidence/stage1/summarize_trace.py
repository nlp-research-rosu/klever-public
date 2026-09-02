#!/usr/bin/env python3
"""Bounded, reviewer-authored summary of every record in the generation trace."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path


def bounded(value: object, limit: int) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    text = text.replace("\x00", "<NUL>")
    if len(text) <= limit:
        return text
    return text[: limit // 2] + f"\n... <{len(text) - limit} chars omitted> ...\n" + text[-limit // 2 :]


def main() -> None:
    paths = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    rows: list[tuple[Path, int, dict[str, object]]] = []
    for path in paths:
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                rows.append((path, line_number, json.loads(line)))

    top = Counter(str(row.get("type")) for _, _, row in rows)
    payload_types = Counter(
        str(row.get("payload", {}).get("type", "<none>"))
        for _, _, row in rows
        if isinstance(row.get("payload"), dict)
    )
    print(f"FILES={len(paths)} RECORDS={len(rows)}")
    print(f"TOP_LEVEL_TYPES={dict(sorted(top.items()))}")
    print(f"PAYLOAD_TYPES={dict(sorted(payload_types.items()))}")

    for path, line_number, row in rows:
        payload = row.get("payload")
        if not isinstance(payload, dict):
            continue
        payload_type = payload.get("type")
        if row.get("type") == "session_meta":
            selected = {
                key: payload.get(key)
                for key in ("id", "session_id", "cwd", "cli_version", "source", "model_provider")
            }
            print(f"\n[{path.name}:{line_number}] SESSION {bounded(selected, 2000)}")
        elif payload_type == "function_call":
            selected = {
                "name": payload.get("name"),
                "call_id": payload.get("call_id"),
                "arguments": payload.get("arguments"),
            }
            print(f"\n[{path.name}:{line_number}] CALL {bounded(selected, 6000)}")
        elif payload_type == "function_call_output":
            selected = {
                "call_id": payload.get("call_id"),
                "output": payload.get("output"),
            }
            print(f"\n[{path.name}:{line_number}] CALL_OUTPUT {bounded(selected, 3000)}")
        elif payload_type == "message":
            role = payload.get("role")
            phase = payload.get("phase")
            content = payload.get("content")
            print(
                f"\n[{path.name}:{line_number}] MESSAGE role={role!r} phase={phase!r} "
                f"{bounded(content, 5000)}"
            )
        elif payload_type in {
            "agent_message",
            "user_message",
            "task_complete",
            "turn_aborted",
            "stream_error",
            "error",
        }:
            print(
                f"\n[{path.name}:{line_number}] EVENT type={payload_type!r} "
                f"{bounded(payload, 5000)}"
            )


if __name__ == "__main__":
    main()
