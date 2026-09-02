"""Bounded structural inspection of all required pipeline-v3 generation records."""

from __future__ import annotations

import collections
import json
from pathlib import Path


def read_json(path: Path):
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


audit = read_json(Path("/audit-input.json"))
print("record_layout", audit["record_layout"])
print("semantics_mode", audit["semantics_mode"])
print("problem_id", audit["problem_id"])

for path in (
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/runtime-metrics.json"),
    Path("/generation-evidence/usage.json"),
):
    record = read_json(path)
    print(
        "json_record",
        path,
        "schema",
        record.get("schema_version"),
        "status",
        record.get("status", "-"),
        "exit",
        record.get("exit_code", record.get("final_exit_code", "-")),
    )

for path in (
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
):
    text = path.read_text(encoding="utf-8")
    print(
        "text_record",
        path,
        "bytes",
        len(text.encode()),
        "lines",
        len(text.splitlines()),
    )
    if path.name == "codex-output.log":
        for needle in (
            " succeeded in ",
            " exited 1 in ",
            "#Top",
            "WarnStuckClaimState",
            "RESULT: KPROVE_PASSED",
        ):
            print("  occurrence", repr(needle), text.count(needle))

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
trace_files = [path for path in trace_files if path.is_file()]
print("trace_file_count", len(trace_files))
for path in trace_files:
    outer_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    tool_names: collections.Counter[str] = collections.Counter()
    line_count = 0
    with path.open(encoding="utf-8") as stream:
        for line_count, line in enumerate(stream, 1):
            event = json.loads(line)
            outer_types[event["type"]] += 1
            payload = event.get("payload", {})
            payload_type = payload.get("type")
            if payload_type:
                payload_types[payload_type] += 1
            if payload_type in {"function_call", "custom_tool_call"}:
                tool_names[payload.get("name", "?")] += 1
    print("trace", path, "json_lines", line_count)
    print("  outer_types", dict(sorted(outer_types.items())))
    print("  payload_types", dict(sorted(payload_types.items())))
    print("  tool_names", dict(sorted(tool_names.items())))
