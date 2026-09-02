#!/usr/bin/env python3
"""Bounded semantic inspection of all required legacy-selected-stage1 records."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


GEN = Path("/generation-evidence")


def load(path: Path):
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    audit = load(Path("/audit-input.json"))
    run = load(Path("/run.json"))
    task = load(Path("/task.json"))
    result = load(Path("/generation-result.json"))
    invocation = load(GEN / "invocation.json")
    metrics = load(GEN / "metrics.json")
    usage = load(GEN / "usage.json")
    prompt = (GEN / "prompt.txt").read_text(encoding="utf-8")
    last = (GEN / "codex-last.txt").read_text(encoding="utf-8")
    output = (GEN / "codex-output.log").read_text(encoding="utf-8")

    print(f"record_layout={audit['record_layout']}")
    print(
        "run="
        f"schema_{run['schema_version']} legacy_import_{run['legacy_import']} "
        f"source_layout_{run['source_layout_version']} model_{run['model']}"
    )
    print(
        "task="
        f"problem_{task['problem_id']} provenance_{task['input_provenance']} "
        f"stage_{task['current_stage']}"
    )
    print(
        "result="
        f"status_{result['status']} marker_{result['result_marker']} "
        f"invocation_{result['invocation']}"
    )
    print(
        "invocation="
        f"status_{invocation['status']} exit_{invocation['exit_code']} "
        f"timeout_{invocation['timeout_marker']} oom_{invocation['oom_killed']}"
    )
    print(
        "metrics="
        f"status_{metrics['status']} exit_{metrics['exit_code']} "
        f"duration_s_{metrics['duration_s']}"
    )
    print(
        "usage="
        f"status_{usage['status']} selected_line_{usage['selected_event']['line_number']} "
        f"total_tokens_{usage['cumulative']['total_tokens']}"
    )
    print(
        "runtime_metrics_present="
        f"{(GEN / 'runtime-metrics.json').exists()} required_for_layout=False"
    )
    print(
        f"prompt_bytes={len(prompt.encode())} prompt_sha256={sha(GEN / 'prompt.txt')} "
        f"has_supplied_semantics_instruction={'provided reference semantics' in prompt}"
    )
    print(f"codex_last_bytes={len(last.encode())} text={last!r}")
    print(
        f"codex_output_lines={len(output.splitlines())} "
        f"codex_output_bytes={len(output.encode())} "
        f"codex_output_sha256={sha(GEN / 'codex-output.log')}"
    )
    for pattern in [
        "#Top",
        "WarnStuckClaimState",
        "[Error] Prover",
        "KPROVE_PASSED",
        "solution.mpy",
        "verification.k",
        "spec.k",
    ]:
        print(f"codex_output_count[{pattern!r}]={output.count(pattern)}")

    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    call_names: collections.Counter[str] = collections.Counter()
    agent_messages: list[tuple[str, str]] = []
    output_top_mentions = 0
    trace_files = sorted((GEN / "codex-trace").rglob("*.jsonl"))
    line_count = 0
    for trace_file in trace_files:
        with trace_file.open("r", encoding="utf-8") as stream:
            for line in stream:
                line_count += 1
                item = json.loads(line)
                top_types[str(item.get("type", "<none>"))] += 1
                payload = item.get("payload") or {}
                payload_type = str(payload.get("type", "<none>"))
                payload_types[payload_type] += 1
                if payload_type in {"function_call", "custom_tool_call"}:
                    call_names[str(payload.get("name", "<none>"))] += 1
                if payload_type == "agent_message":
                    agent_messages.append(
                        (str(payload.get("phase")), str(payload.get("message")))
                    )
                if payload_type in {"function_call_output", "custom_tool_call_output"}:
                    if "#Top" in json.dumps(payload, ensure_ascii=False):
                        output_top_mentions += 1
    print(
        f"trace_files={len(trace_files)} trace_lines={line_count} malformed_lines=0"
    )
    print(f"trace_top_types={dict(sorted(top_types.items()))}")
    print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
    print(f"trace_call_names={dict(sorted(call_names.items()))}")
    print(f"trace_tool_outputs_with_Top={output_top_mentions}")
    print(f"trace_agent_message_count={len(agent_messages)}")
    if agent_messages:
        phase, message = agent_messages[-1]
        print(f"trace_last_agent_phase={phase}")
        print(f"trace_last_agent_message={message!r}")
    print("GENERATION_RECORD_INSPECTION=PASS")


if __name__ == "__main__":
    main()
