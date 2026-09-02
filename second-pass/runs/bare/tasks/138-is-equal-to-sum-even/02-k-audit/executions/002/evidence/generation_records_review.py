#!/usr/bin/env python3
"""Parse every required legacy-selected-stage1 generation record."""

from __future__ import annotations

import collections
import json
from pathlib import Path


def main() -> int:
    records = {
        "run": Path("/run.json"),
        "task": Path("/task.json"),
        "result": Path("/generation-result.json"),
        "invocation": Path("/generation-evidence/invocation.json"),
        "metrics": Path("/generation-evidence/metrics.json"),
        "usage": Path("/generation-evidence/usage.json"),
    }
    parsed = {name: json.loads(path.read_text()) for name, path in records.items()}
    print("record_layout: legacy-selected-stage1")
    print("run:", {
        "schema_version": parsed["run"]["schema_version"],
        "legacy_import": parsed["run"]["legacy_import"],
        "config": parsed["run"]["config"],
    })
    print("task:", {
        "problem_id": parsed["task"]["problem_id"],
        "condition": parsed["task"]["condition"],
        "input_provenance": parsed["task"]["input_provenance"],
        "inputs": parsed["task"]["inputs"],
    })
    print("result:", {
        "status": parsed["result"]["status"],
        "result_marker": parsed["result"]["result_marker"],
        "invocation": parsed["result"]["invocation"],
    })
    print("invocation:", {
        "status": parsed["invocation"]["status"],
        "exit_code": parsed["invocation"]["exit_code"],
        "legacy_import": parsed["invocation"]["legacy_import"],
        "workspace_sha256": parsed["invocation"]["outputs"]["workspace_sha256"],
    })
    print("metrics:", parsed["metrics"])
    print("usage:", {
        "status": parsed["usage"]["status"],
        "selected_event": parsed["usage"]["selected_event"],
        "source_trace_sha256": parsed["usage"]["source_trace_sha256"],
        "cumulative": parsed["usage"]["cumulative"],
    })

    text_records = [
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    for path in text_records:
        text = path.read_text(errors="replace")
        print(
            "text_record:",
            path.name,
            "bytes=",
            len(text.encode()),
            "lines=",
            len(text.splitlines()),
            "mentions_kprove=",
            text.count("kprove"),
            "mentions_Top=",
            text.count("#Top"),
        )

    trace_path = next(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    counts: collections.Counter[tuple[str | None, str | None]] = collections.Counter()
    tool_calls = []
    lines = trace_path.read_text().splitlines()
    for number, line in enumerate(lines, 1):
        event = json.loads(line)
        payload = event.get("payload")
        payload_type = payload.get("type") if isinstance(payload, dict) else None
        counts[(event.get("type"), payload_type)] += 1
        if payload_type == "custom_tool_call":
            tool_input = payload.get("input", "")
            first_line = tool_input.splitlines()[0] if isinstance(tool_input, str) else str(tool_input)
            tool_calls.append((number, payload.get("name"), first_line[:240]))
    print("trace_path:", trace_path)
    print("trace_line_count:", len(lines))
    print("trace_event_counts:", sorted((str(k), v) for k, v in counts.items()))
    print("trace_custom_tool_call_count:", len(tool_calls))
    for call in tool_calls:
        print("trace_call:", call)
    assert len(lines) == 138
    assert parsed["usage"]["selected_event"]["line_number"] == 137
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
