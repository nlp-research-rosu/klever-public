#!/usr/bin/env python3
"""Read and summarize every required legacy-selected-stage1 record."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path("/generation-evidence")
TRACE = next((ROOT / "codex-trace").rglob("*.jsonl"))
RECORDS = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    ROOT / "invocation.json",
    ROOT / "metrics.json",
    ROOT / "usage.json",
]
TEXT = [
    ROOT / "codex-last.txt",
    ROOT / "codex-output.log",
    ROOT / "prompt.txt",
]


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    for path in RECORDS:
        raw = path.read_bytes()
        parsed = json.loads(raw)
        print(
            f"JSON {path} bytes={len(raw)} sha256={digest(raw)} "
            f"top_keys={sorted(parsed)}"
        )

    for path in TEXT:
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        print(
            f"TEXT {path} bytes={len(raw)} lines={len(text.splitlines())} "
            f"sha256={digest(raw)} nul_bytes={raw.count(bytes([0]))}"
        )

    counts: dict[str, int] = {}
    tool_inputs: list[str] = []
    line_count = 0
    for line_count, line in enumerate(TRACE.read_text(encoding="utf-8").splitlines(), 1):
        item = json.loads(line)
        payload = item.get("payload", {})
        key = f"{item.get('type')}/{payload.get('type')}"
        counts[key] = counts.get(key, 0) + 1
        if payload.get("type") == "function_call":
            tool_inputs.append(payload.get("arguments", ""))
        if payload.get("type") == "custom_tool_call":
            tool_inputs.append(payload.get("input", ""))
    print(
        f"TRACE {TRACE} lines={line_count} bytes={TRACE.stat().st_size} "
        f"sha256={digest(TRACE.read_bytes())}"
    )
    for key, count in sorted(counts.items()):
        print(f"TRACE_EVENT {key} {count}")

    joined = "\n".join(tool_inputs)
    print(f"TOOL_INPUT_COUNT {len(tool_inputs)}")
    print(
        "REFERENCE_SEMANTICS_PATCH_MENTIONS "
        f"{joined.count('*** Update File: /work/reference-semantics') + joined.count('*** Add File: /work/reference-semantics')}"
    )
    print(f"KPROVE_COMMAND_MENTIONS {joined.count('kprove ')}")
    print(f"KOMPILE_COMMAND_MENTIONS {joined.count('kompile ')}")
    print(f"APPLY_PATCH_MENTIONS {joined.count('*** Begin Patch')}")


if __name__ == "__main__":
    main()
