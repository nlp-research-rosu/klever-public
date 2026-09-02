#!/usr/bin/env python3
"""Read and structurally summarize every required pipeline-v3 generation record."""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--trace", type=Path, required=True)
    args = parser.parse_args()

    required_json = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        args.root / "invocation.json",
        args.root / "metrics.json",
        args.root / "runtime-metrics.json",
        args.root / "usage.json",
    ]
    required_text = [
        args.root / "codex-last.txt",
        args.root / "codex-output.log",
        args.root / "prompt.txt",
    ]

    for path in required_json:
        value = json.loads(path.read_text())
        print(
            "JSON",
            path,
            f"sha256={sha256(path)}",
            f"top_keys={','.join(sorted(value))}",
        )

    for path in required_text:
        text = path.read_text()
        print(
            "TEXT",
            path,
            f"sha256={sha256(path)}",
            f"lines={len(text.splitlines())}",
            f"chars={len(text)}",
            f"nul_bytes={text.count(chr(0))}",
        )
        if path.name == "codex-output.log":
            for token in [
                "#Top",
                "WarnStuckClaimState",
                "kompile",
                "kprove",
                "RESULT:",
                "VALIDATED",
            ]:
                print("OUTPUT_TOKEN", repr(token), f"count={text.count(token)}")

    event_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    call_names: collections.Counter[str] = collections.Counter()
    command_digests: list[tuple[int, str, str]] = []
    final_messages: list[str] = []
    parsed = 0

    with args.trace.open() as stream:
        for line_number, line in enumerate(stream, 1):
            event = json.loads(line)
            parsed += 1
            event_type = str(event.get("type"))
            event_types[event_type] += 1
            payload = event.get("payload")
            if isinstance(payload, dict):
                payload_type = payload.get("type")
                if payload_type is not None:
                    payload_types[str(payload_type)] += 1
                if event_type == "response_item" and payload_type == "function_call":
                    name = str(payload.get("name"))
                    call_names[name] += 1
                    arguments = str(payload.get("arguments", ""))
                    if name in {"exec_command", "write_stdin"}:
                        command_digests.append(
                            (
                                line_number,
                                name,
                                hashlib.sha256(arguments.encode()).hexdigest(),
                            )
                        )
                if payload_type == "agent_message" and payload.get("phase") == "final_answer":
                    final_messages.append(str(payload.get("message", "")))

    print(
        "TRACE",
        args.trace,
        f"sha256={sha256(args.trace)}",
        f"parsed_json_lines={parsed}",
        f"event_types={dict(sorted(event_types.items()))}",
        f"payload_types={dict(sorted(payload_types.items()))}",
        f"function_calls={dict(sorted(call_names.items()))}",
        f"shell_call_count={len(command_digests)}",
    )
    for line_number, name, digest in command_digests:
        print("TRACE_SHELL_CALL", line_number, name, digest)
    for index, message in enumerate(final_messages):
        print("TRACE_FINAL", index, repr(message))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
