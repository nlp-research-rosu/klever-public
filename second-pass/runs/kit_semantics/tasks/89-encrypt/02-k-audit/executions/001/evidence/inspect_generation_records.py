#!/usr/bin/env python3
"""Parse every required pipeline-v3 generation record as untrusted evidence."""

from __future__ import annotations

import collections
import json
from pathlib import Path


ROOT = Path("/generation-evidence")


def line_count(path: Path) -> int:
    with path.open("rb") as stream:
        return sum(1 for _ in stream)


def main() -> None:
    required = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        ROOT / "invocation.json",
        ROOT / "metrics.json",
        ROOT / "runtime-metrics.json",
        ROOT / "usage.json",
        ROOT / "codex-last.txt",
        ROOT / "codex-output.log",
        ROOT / "prompt.txt",
    ]
    for path in required:
        data = path.read_bytes()
        print(f"record={path} bytes={len(data)} lines={line_count(path)}")
        if path.suffix == ".json":
            parsed = json.loads(data)
            assert isinstance(parsed, dict)

    trace_files = sorted((ROOT / "codex-trace").rglob("*"))
    trace_files = [path for path in trace_files if path.is_file()]
    assert len(trace_files) == 1
    event_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    function_calls: collections.Counter[str] = collections.Counter()
    shell_commands: list[str] = []
    patch_calls = 0
    assistant_final = None

    for trace_path in trace_files:
        with trace_path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                event = json.loads(line)
                event_types[event["type"]] += 1
                payload = event.get("payload", {})
                if isinstance(payload, dict) and isinstance(payload.get("type"), str):
                    payload_types[payload["type"]] += 1
                if event["type"] == "response_item" and payload.get("type") == "function_call":
                    name = payload.get("name", "<missing>")
                    function_calls[name] += 1
                    arguments_text = payload.get("arguments", "{}")
                    if name == "exec_command":
                        arguments = json.loads(arguments_text)
                        shell_commands.append(arguments.get("cmd", "<missing cmd>"))
                    elif name == "apply_patch":
                        patch_calls += 1
                if event["type"] == "event_msg" and payload.get("type") == "agent_message":
                    if payload.get("phase") == "final_answer":
                        assistant_final = payload.get("message")
        print(
            f"trace={trace_path} bytes={trace_path.stat().st_size} "
            f"lines={line_count(trace_path)}"
        )

    print(f"trace_event_types={dict(sorted(event_types.items()))}")
    print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
    print(f"trace_function_calls={dict(sorted(function_calls.items()))}")
    print(f"trace_apply_patch_calls={patch_calls}")
    print(f"trace_exec_command_count={len(shell_commands)}")
    for index, command in enumerate(shell_commands, 1):
        single_line = " ".join(command.split())
        print(f"trace_exec[{index}]={single_line[:500]}")
    assert assistant_final is not None
    print("trace_final_message=" + " ".join(assistant_final.split())[:1000])

    output_text = (ROOT / "codex-output.log").read_text(
        encoding="utf-8", errors="replace"
    )
    for marker in [
        "#Top",
        "WarnStuckClaimState",
        "EXPECTED FAILURE",
        "VALIDATED",
        "RESULT: KPROVE_PASSED",
    ]:
        print(f"codex_output_marker[{marker}]={output_text.count(marker)}")
    print("GENERATION_RECORD_INSPECTION=COMPLETE_UNTRUSTED")


if __name__ == "__main__":
    main()
