#!/usr/bin/env python3
"""Read an untrusted Codex JSONL trace and emit a bounded factual inventory."""

from __future__ import annotations

import collections
import hashlib
import json
import pathlib
import sys


def bounded(value: object, limit: int = 1800) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    text = text.replace("\x00", "\\0")
    if len(text) <= limit:
        return text
    return text[:limit] + f"... <{len(text) - limit} chars omitted>"


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} TRACE.jsonl", file=sys.stderr)
        return 64
    path = pathlib.Path(sys.argv[1])
    raw = path.read_bytes()
    counts: collections.Counter[tuple[str, str]] = collections.Counter()
    items: list[tuple[int, str, str]] = []
    errors: list[str] = []
    for line_number, raw_line in enumerate(raw.splitlines(), 1):
        try:
            record = json.loads(raw_line)
        except Exception as exc:
            errors.append(f"line {line_number}: {exc}")
            continue
        outer_type = str(record.get("type", ""))
        payload = record.get("payload", {})
        inner_type = str(payload.get("type", "")) if isinstance(payload, dict) else ""
        counts[(outer_type, inner_type)] += 1
        if outer_type != "response_item" or not isinstance(payload, dict):
            continue
        if inner_type == "message":
            role = str(payload.get("role", ""))
            if role not in {"assistant", "user"}:
                continue
            content_texts = []
            for content in payload.get("content", []):
                if not isinstance(content, dict):
                    continue
                for key in ("text", "input_text", "output_text"):
                    if key in content:
                        content_texts.append(str(content[key]))
                        break
            items.append((line_number, f"MESSAGE role={role}", "\n".join(content_texts)))
        elif inner_type in {
            "function_call",
            "function_call_output",
            "custom_tool_call",
            "custom_tool_call_output",
            "local_shell_call",
        }:
            label = inner_type
            name = payload.get("name") or payload.get("call_id") or payload.get("id") or ""
            items.append((line_number, f"{label} {name}", payload))

    print(f"PATH: {path}")
    print(f"BYTES: {len(raw)}")
    print(f"SHA256: {hashlib.sha256(raw).hexdigest()}")
    print(f"LINES: {len(raw.splitlines())}")
    print(f"JSON_ERRORS: {len(errors)}")
    for error in errors:
        print(f"  {error}")
    print("EVENT_COUNTS:")
    for (outer_type, inner_type), count in sorted(counts.items()):
        print(f"  {count:4d} | {outer_type} | {inner_type}")
    print("UNTRUSTED_MESSAGES_AND_TOOL_RECORDS:")
    for line_number, label, value in items:
        print(f"--- line {line_number}: {label} ---")
        print(bounded(value))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
