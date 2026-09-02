#!/usr/bin/env python3
"""Read and summarize every required legacy-selected-stage1 generation record."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path("/generation-evidence")


def clipped(value: object, limit: int = 320) -> str:
    text = str(value).replace("\r", "\\r").replace("\n", "\\n")
    return text if len(text) <= limit else text[:limit] + "...<clipped>"


def main() -> None:
    required_json = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        ROOT / "invocation.json",
        ROOT / "metrics.json",
    ]
    optional_json = [ROOT / "usage.json"]
    for path in required_json + [p for p in optional_json if p.exists()]:
        document = json.loads(path.read_text())
        print(
            f"JSON_OK path={path} top_type={type(document).__name__} "
            f"top_keys={sorted(document) if isinstance(document, dict) else 'n/a'}"
        )

    prompt = (ROOT / "prompt.txt").read_text()
    last = (ROOT / "codex-last.txt").read_text()
    output = (ROOT / "codex-output.log").read_text()
    print(f"PROMPT_READ chars={len(prompt)} lines={len(prompt.splitlines())}")
    print(f"CODEX_LAST_READ chars={len(last)} lines={len(last.splitlines())}")
    print(f"CODEX_OUTPUT_READ chars={len(output)} lines={len(output.splitlines())}")
    print(f"CODEX_LAST={clipped(last, 1200)}")
    markers = {
        "#Top": output.count("#Top"),
        "KPROVE_PASSED": output.count("KPROVE_PASSED"),
        "kprove": output.count("kprove"),
        "kompile": output.count("kompile"),
        "krun": output.count("krun"),
        "WarnStuckClaimState": output.count("WarnStuckClaimState"),
        "[Error]": output.count("[Error]"),
    }
    print(f"CODEX_OUTPUT_MARKER_COUNTS={markers}")

    top_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    function_names: Counter[str] = Counter()
    trace_records = 0
    calls: list[tuple[str, str, str]] = []
    assistant_messages: list[str] = []
    for trace_path in sorted((ROOT / "codex-trace").rglob("*.jsonl")):
        relative = trace_path.relative_to(ROOT)
        with trace_path.open() as stream:
            for line_number, line in enumerate(stream, 1):
                item = json.loads(line)
                trace_records += 1
                top_types[str(item.get("type"))] += 1
                payload = item.get("payload")
                if not isinstance(payload, dict):
                    continue
                payload_type = str(payload.get("type"))
                payload_types[payload_type] += 1
                if payload_type in {"function_call", "custom_tool_call"}:
                    name = str(payload.get("name"))
                    function_names[name] += 1
                    arguments = payload.get("arguments", payload.get("input", ""))
                    calls.append((f"{relative}:{line_number}", name, clipped(arguments)))
                if payload_type == "message" and payload.get("role") == "assistant":
                    content = payload.get("content")
                    assistant_messages.append(clipped(content, 1200))
    print(f"TRACE_RECORDS_READ={trace_records}")
    print(f"TRACE_TOP_TYPES={dict(sorted(top_types.items()))}")
    print(f"TRACE_PAYLOAD_TYPES={dict(sorted(payload_types.items()))}")
    print(f"TRACE_FUNCTION_NAMES={dict(sorted(function_names.items()))}")
    print(f"TRACE_FUNCTION_CALLS={len(calls)}")
    for location, name, arguments in calls:
        print(f"CALL location={location} name={name} args={arguments}")
    print(f"TRACE_ASSISTANT_MESSAGES={len(assistant_messages)}")
    for index, message in enumerate(assistant_messages, 1):
        print(f"ASSISTANT_MESSAGE[{index}]={message}")


if __name__ == "__main__":
    main()
