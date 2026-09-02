#!/usr/bin/env python3
"""Parse every structured trace record and summarize untrusted generation claims."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    root = Path("/generation-evidence")
    traces = sorted((root / "codex-trace").rglob("*"))
    trace_files = [path for path in traces if path.is_file()]
    print(f"trace_files={len(trace_files)}")
    malformed = 0
    total = 0
    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    tool_names: collections.Counter[str] = collections.Counter()
    final_messages: list[str] = []
    for path in trace_files:
        print(f"trace={path.relative_to(root)} bytes={path.stat().st_size} sha256={digest(path)}")
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                total += 1
                try:
                    item = json.loads(line)
                except ValueError:
                    malformed += 1
                    print(f"malformed_json={path}:{line_number}")
                    continue
                top_types[str(item.get("type"))] += 1
                payload = item.get("payload")
                if isinstance(payload, dict):
                    payload_types[str(payload.get("type"))] += 1
                    name = payload.get("name")
                    if isinstance(name, str):
                        tool_names[name] += 1
                    if payload.get("type") == "message" and payload.get("role") == "assistant":
                        content = payload.get("content")
                        if isinstance(content, list):
                            for block in content:
                                if (
                                    isinstance(block, dict)
                                    and block.get("type") in {"output_text", "text"}
                                    and isinstance(block.get("text"), str)
                                ):
                                    final_messages.append(block["text"])
    print(f"trace_lines={total}")
    print(f"malformed_trace_lines={malformed}")
    print("top_types=" + json.dumps(top_types, sort_keys=True))
    print("payload_types=" + json.dumps(payload_types, sort_keys=True))
    print("tool_names=" + json.dumps(tool_names, sort_keys=True))

    for name in (
        "invocation.json",
        "metrics.json",
        "usage.json",
        "legacy-metrics.json",
        "legacy-run-input.json",
        "prompt.txt",
        "codex-last.txt",
        "codex-output.log",
    ):
        path = root / name
        if path.exists():
            data = path.read_bytes()
            print(f"record={name} bytes={len(data)} sha256={hashlib.sha256(data).hexdigest()}")

    output = (root / "codex-output.log").read_text(encoding="utf-8", errors="replace")
    last = (root / "codex-last.txt").read_text(encoding="utf-8", errors="replace")
    print(f"codex_output_has_top={('#Top' in output)}")
    print(f"codex_output_has_result_marker={('RESULT: KPROVE_PASSED' in output)}")
    print(f"codex_last_matches_output_suffix={output.rstrip().endswith(last.rstrip())}")
    print(f"assistant_text_blocks={len(final_messages)}")
    return 1 if malformed else 0


if __name__ == "__main__":
    raise SystemExit(main())
