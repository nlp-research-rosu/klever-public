#!/usr/bin/env python3
"""Inventory every structured generation-trace record without trusting it."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def short(text: str, limit: int = 500) -> str:
    text = text.replace("\n", "\\n")
    return text if len(text) <= limit else text[:limit] + "...<truncated>"


def main() -> int:
    files = sorted(TRACE_ROOT.rglob("*"))
    regular_files = [path for path in files if path.is_file() and not path.is_symlink()]
    symlinks = [path for path in files if path.is_symlink()]
    print(f"regular_trace_files={len(regular_files)} symlinks={len(symlinks)}")
    type_counts: collections.Counter[str] = collections.Counter()
    payload_counts: collections.Counter[str] = collections.Counter()
    role_counts: collections.Counter[str] = collections.Counter()
    calls: list[tuple[int, str, str]] = []
    call_outputs: list[tuple[int, str]] = []
    assistant_messages: list[tuple[int, str]] = []
    total_lines = 0
    for path in regular_files:
        relative = path.relative_to(TRACE_ROOT)
        print(f"trace_file={relative} sha256={sha256_file(path)} bytes={path.stat().st_size}")
        with path.open() as stream:
            for line_number, line in enumerate(stream, 1):
                total_lines += 1
                record = json.loads(line)
                record_type = str(record.get("type"))
                type_counts[record_type] += 1
                payload = record.get("payload", {})
                if isinstance(payload, dict):
                    payload_type = str(payload.get("type"))
                    payload_counts[payload_type] += 1
                    if payload_type == "message":
                        role = str(payload.get("role"))
                        role_counts[role] += 1
                        texts = []
                        for item in payload.get("content", []):
                            if isinstance(item, dict) and "text" in item:
                                texts.append(str(item["text"]))
                        if role == "assistant":
                            assistant_messages.append((line_number, "\n".join(texts)))
                    elif payload_type in {"function_call", "custom_tool_call"}:
                        name = str(payload.get("name"))
                        args = payload.get("arguments", payload.get("input", ""))
                        calls.append((line_number, name, str(args)))
                    elif payload_type in {"function_call_output", "custom_tool_call_output"}:
                        output = payload.get("output", "")
                        call_outputs.append((line_number, str(output)))
    print(f"total_jsonl_lines={total_lines}")
    print(f"record_type_counts={dict(sorted(type_counts.items()))}")
    print(f"payload_type_counts={dict(sorted(payload_counts.items()))}")
    print(f"message_role_counts={dict(sorted(role_counts.items()))}")
    print(f"tool_calls={len(calls)} tool_outputs={len(call_outputs)}")
    for line_number, name, args in calls:
        print(f"CALL line={line_number} name={name} args={short(args, 1000)}")
    for line_number, message in assistant_messages:
        print(f"ASSISTANT line={line_number} text={short(message, 1500)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
