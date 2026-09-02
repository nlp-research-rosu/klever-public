#!/usr/bin/env python3
"""Read and structurally inspect every pipeline-v3 generation record."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

JSON_FILES = [
    Path("/audit-input.json"),
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation/invocation.json"),
    Path("/generation/metrics.json"),
    Path("/generation/runtime-metrics.json"),
    Path("/generation/usage.json"),
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


for path in JSON_FILES:
    value = json.loads(path.read_text(encoding="utf-8"))
    print(
        f"json_ok path={path} type={type(value).__name__} "
        f"sha256={digest(path)}"
    )

trace_files = sorted(Path("/generation/codex-trace").rglob("*"))
trace_files = [path for path in trace_files if path.is_file()]
print(f"trace_file_count={len(trace_files)}")
for path in trace_files:
    event_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    tool_names: Counter[str] = Counter()
    line_count = 0
    for line_count, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        event = json.loads(line)
        event_types[str(event.get("type", "NO_TYPE"))] += 1
        payload = event.get("payload")
        if isinstance(payload, dict):
            payload_type = str(payload.get("type", "NO_PAYLOAD_TYPE"))
            payload_types[payload_type] += 1
            if payload_type == "function_call":
                tool_names[str(payload.get("name", "NO_NAME"))] += 1
    print(
        f"trace_ok path={path} lines={line_count} sha256={digest(path)}"
    )
    print(f"trace_event_types={dict(sorted(event_types.items()))}")
    print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
    print(f"trace_tool_names={dict(sorted(tool_names.items()))}")

output_path = Path("/generation/codex-output.log")
output_text = output_path.read_text(encoding="utf-8")
print(
    f"generation_output_utf8_ok lines={len(output_text.splitlines())} "
    f"chars={len(output_text)} nul_count={output_text.count(chr(0))} "
    f"sha256={digest(output_path)}"
)
for needle in (
    "kprove spec.k",
    "#Top",
    "spec-vacuity.k",
    "differential_test.py",
    "RESULT: KPROVE_PASSED",
):
    print(f"generation_output_occurrences {needle!r}={output_text.count(needle)}")
