#!/usr/bin/env python3
"""Read the complete structured generation trace and summarize untrusted claims."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


ROOT = Path("/generation-evidence")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compact(value: object, limit: int = 1000) -> str:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return text if len(text) <= limit else text[:limit] + "...[bounded]"


def main() -> None:
    for name in (
        "invocation.json",
        "metrics.json",
        "legacy-metrics.json",
        "legacy-run-input.json",
        "usage.json",
    ):
        path = ROOT / name
        record = json.loads(path.read_text())
        print(f"RECORD {name} sha256={digest(path)}")
        print(compact(record, 1600))

    for name in ("prompt.txt", "codex-last.txt", "codex-output.log"):
        path = ROOT / name
        lines = path.read_text(errors="replace").splitlines()
        print(
            f"TEXT {name} sha256={digest(path)} bytes={path.stat().st_size} "
            f"lines={len(lines)}"
        )
        if name != "codex-output.log":
            print("BEGIN")
            print("\n".join(lines))
            print("END")
        else:
            signals = collections.Counter()
            for line in lines:
                if "#Top" in line:
                    signals["#Top-lines"] += 1
                if "exited with code 0" in line or "succeeded in " in line:
                    signals["success-status-lines"] += 1
                if "exited with code" in line and "code 0" not in line:
                    signals["nonzero-status-lines"] += 1
                if "timed out" in line.lower():
                    signals["timeout-lines"] += 1
            print(f"codex-output-signals={dict(signals)}")

    trace_files = sorted((ROOT / "codex-trace").rglob("*.jsonl"))
    print(f"trace_file_count={len(trace_files)}")
    for path in trace_files:
        outer = collections.Counter()
        payload_types = collections.Counter()
        commands: list[str] = []
        command_outputs: list[str] = []
        assistant_messages: list[str] = []
        malformed: list[str] = []
        with path.open(errors="replace") as src:
            for line_no, line in enumerate(src, 1):
                try:
                    event = json.loads(line)
                except json.JSONDecodeError as err:
                    malformed.append(f"line {line_no}: {err}")
                    continue
                outer[str(event.get("type"))] += 1
                payload = event.get("payload", {})
                if isinstance(payload, dict):
                    ptype = str(payload.get("type"))
                    payload_types[ptype] += 1
                    if ptype in ("function_call", "custom_tool_call"):
                        commands.append(
                            f"line={line_no} name={payload.get('name')} "
                            f"arguments={compact(payload.get('arguments') or payload.get('input'), 1800)}"
                        )
                    elif ptype in ("function_call_output", "custom_tool_call_output"):
                        output = payload.get("output")
                        command_outputs.append(
                            f"line={line_no} call_id={payload.get('call_id')} "
                            f"output={compact(output, 1000)}"
                        )
                    elif ptype == "message" and payload.get("role") == "assistant":
                        texts = []
                        for item in payload.get("content", []):
                            if isinstance(item, dict) and "text" in item:
                                texts.append(str(item["text"]))
                        if texts:
                            assistant_messages.append(
                                f"line={line_no} " + " ".join(texts)
                            )
        print(
            f"TRACE {path.relative_to(ROOT)} sha256={digest(path)} "
            f"bytes={path.stat().st_size}"
        )
        print(f"outer_types={dict(outer)}")
        print(f"payload_types={dict(payload_types)}")
        print(f"malformed_count={len(malformed)}")
        for item in malformed:
            print(f"MALFORMED {item}")
        print(f"tool_call_count={len(commands)}")
        for command in commands:
            print(f"TOOL_CALL {command}")
        print(f"tool_output_count={len(command_outputs)}")
        for output in command_outputs:
            print(f"TOOL_OUTPUT {output}")
        print(f"assistant_message_count={len(assistant_messages)}")
        for message in assistant_messages:
            print(f"ASSISTANT {message}")


if __name__ == "__main__":
    main()
