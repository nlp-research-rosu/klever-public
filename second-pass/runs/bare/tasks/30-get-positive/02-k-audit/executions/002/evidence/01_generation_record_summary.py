#!/usr/bin/env python3
"""Bounded structural summary of all required legacy-selected-stage1 records."""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path


def load(path: str):
    return json.loads(Path(path).read_text())


def main() -> int:
    audit = load("/audit-input.json")
    run = load("/run.json")
    task = load("/task.json")
    result = load("/generation-result.json")
    invocation = load("/generation-evidence/invocation.json")
    metrics = load("/generation-evidence/metrics.json")
    usage = load("/generation-evidence/usage.json")
    last = Path("/generation-evidence/codex-last.txt").read_text()
    output = Path("/generation-evidence/codex-output.log").read_text()
    prompt = Path("/generation-evidence/prompt.txt").read_text()
    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))

    print(
        "MANIFESTS "
        f"layout={audit['record_layout']} run_schema={run['schema_version']} "
        f"task_stage={task['current_stage']} task_provenance={task['input_provenance']} "
        f"result_status={result['status']} result_marker={result['result_marker']} "
        f"invocation_status={invocation['status']} invocation_exit={invocation['exit_code']} "
        f"metrics_status={metrics['status']} metrics_exit={metrics['exit_code']} "
        f"usage_status={usage['status']}"
    )
    print(
        "IDENTITY "
        f"problem={task['problem_id']} condition={task['condition']['name']} "
        f"config={run['config']} session_result={result['session_id']} "
        f"session_invocation={invocation['session_id']}"
    )
    print(
        "TEXT_RECORDS "
        f"prompt_chars={len(prompt)} last_chars={len(last)} output_chars={len(output)} "
        f"output_top_mentions={len(re.findall(r'#Top', output))} "
        f"output_stuck_mentions={len(re.findall(r'WarnStuckClaimState', output))} "
        f"last_result_marker={'RESULT: KPROVE_PASSED' in last}"
    )
    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[tuple[str, str]] = collections.Counter()
    custom_calls = []
    line_count = 0
    for trace_file in trace_files:
        with trace_file.open() as stream:
            for line_number, line in enumerate(stream, 1):
                line_count += 1
                event = json.loads(line)
                top_type = str(event.get("type"))
                payload_type = str(event.get("payload", {}).get("type"))
                top_types[top_type] += 1
                payload_types[(top_type, payload_type)] += 1
                payload = event.get("payload", {})
                if top_type == "response_item" and payload_type == "custom_tool_call":
                    custom_calls.append(
                        (
                            trace_file.relative_to(
                                Path("/generation-evidence/codex-trace")
                            ).as_posix(),
                            line_number,
                            payload.get("name"),
                        )
                    )
    print(
        f"TRACE files={len(trace_files)} jsonl_lines={line_count} "
        f"top_types={dict(sorted(top_types.items()))}"
    )
    print(
        "TRACE payload_types="
        + repr(dict(sorted(payload_types.items(), key=lambda item: repr(item[0]))))
    )
    print(f"TRACE custom_calls={custom_calls!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
