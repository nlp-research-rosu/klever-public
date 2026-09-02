#!/usr/bin/env python3
"""Bounded inspection summary for every pipeline-v3 generation record."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


def load(path: str):
    return json.loads(Path(path).read_text())


def main() -> None:
    records = {
        "run": load("/run.json"),
        "task": load("/task.json"),
        "generation_result": load("/generation-result.json"),
        "invocation": load("/generation-evidence/invocation.json"),
        "metrics": load("/generation-evidence/metrics.json"),
        "runtime_metrics": load("/generation-evidence/runtime-metrics.json"),
        "usage": load("/generation-evidence/usage.json"),
    }
    for name, record in records.items():
        print(f"{name}={json.dumps(record, sort_keys=True)}")

    last = Path("/generation-evidence/codex-last.txt").read_text()
    prompt = Path("/generation-evidence/prompt.txt").read_text()
    output_lines = Path("/generation-evidence/codex-output.log").read_text().splitlines()
    print(f"codex_last={last!r}")
    print(f"generation_prompt_first_line={prompt.splitlines()[0]!r}")
    print(f"codex_output_lines={len(output_lines)}")
    command_pattern = re.compile(r"^/bin/bash -lc .* in /workspace$")
    output_commands = [
        line for line in output_lines if command_pattern.match(line)
    ]
    print(f"codex_output_shell_command_count={len(output_commands)}")
    for index, command in enumerate(output_commands, 1):
        print(f"codex_output_command[{index}]={command}")

    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    for trace in trace_files:
        top_types: Counter[str] = Counter()
        payload_types: Counter[str] = Counter()
        function_calls: list[tuple[str, object]] = []
        final_messages: list[str] = []
        with trace.open() as stream:
            for line in stream:
                event = json.loads(line)
                top_types[str(event.get("type"))] += 1
                payload = event.get("payload")
                if not isinstance(payload, dict):
                    continue
                payload_type = str(payload.get("type"))
                payload_types[payload_type] += 1
                if payload_type == "function_call":
                    arguments = payload.get("arguments")
                    try:
                        arguments = json.loads(arguments)
                    except (TypeError, json.JSONDecodeError):
                        pass
                    function_calls.append((str(payload.get("name")), arguments))
                if payload_type == "message" and payload.get("role") == "assistant":
                    content = payload.get("content")
                    if isinstance(content, list):
                        for item in content:
                            if isinstance(item, dict) and item.get("type") == "output_text":
                                final_messages.append(str(item.get("text")))
        print(f"trace={trace}")
        print(f"trace_top_types={dict(sorted(top_types.items()))}")
        print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
        print(f"trace_function_call_count={len(function_calls)}")
        for index, (name, arguments) in enumerate(function_calls, 1):
            print(
                f"trace_function_call[{index}]="
                f"{name} {json.dumps(arguments, sort_keys=True)}"
            )
        print(f"trace_assistant_output_messages={len(final_messages)}")
        for message in final_messages:
            print(f"trace_assistant_output={message!r}")


if __name__ == "__main__":
    main()
