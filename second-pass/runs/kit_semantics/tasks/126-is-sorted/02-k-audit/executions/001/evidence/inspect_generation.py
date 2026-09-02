#!/usr/bin/env python3
"""Read and summarize all pipeline-v3 generation records as untrusted evidence."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


ROOT = Path("/generation-evidence")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clipped(value: str, limit: int = 1800) -> str:
    if len(value) <= limit:
        return value
    half = limit // 2
    return (
        value[:half]
        + f"\n...[clipped {len(value) - limit} characters]...\n"
        + value[-half:]
    )


def main() -> int:
    for path in (
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        ROOT / "invocation.json",
        ROOT / "metrics.json",
        ROOT / "runtime-metrics.json",
        ROOT / "usage.json",
    ):
        record = json.loads(path.read_text())
        print(f"JSON_RECORD {path}")
        print(json.dumps(record, indent=2, sort_keys=True))

    result = json.loads(Path("/generation-result.json").read_text())
    evidence_hashes = result["outputs"]["evidence"]
    evidence_failures: list[str] = []
    for rel, expected in sorted(evidence_hashes.items()):
        path = ROOT / rel
        actual = sha256_file(path)
        matched = actual == expected
        print(
            f"RESULT_EVIDENCE_HASH {rel}: actual={actual} "
            f"expected={expected} match={matched}"
        )
        if not matched:
            evidence_failures.append(rel)

    trace_files = sorted((ROOT / "codex-trace").rglob("*"))
    trace_files = [path for path in trace_files if path.is_file()]
    outer_types: collections.Counter[str | None] = collections.Counter()
    payload_types: collections.Counter[str | None] = collections.Counter()
    function_calls: list[tuple[int, str, str]] = []
    function_outputs: dict[str, tuple[int, str]] = {}
    agent_messages: list[tuple[int, str]] = []
    malformed: list[str] = []
    trace_lines = 0

    for trace_path in trace_files:
        print(
            f"TRACE_FILE {trace_path} sha256={sha256_file(trace_path)} "
            f"bytes={trace_path.stat().st_size}"
        )
        with trace_path.open() as stream:
            for line_number, line in enumerate(stream, 1):
                trace_lines += 1
                try:
                    item = json.loads(line)
                except json.JSONDecodeError as err:
                    malformed.append(f"{trace_path}:{line_number}: {err}")
                    continue
                outer_types[item.get("type")] += 1
                payload = item.get("payload", {})
                payload_type = payload.get("type")
                payload_types[payload_type] += 1
                if payload_type == "function_call":
                    function_calls.append(
                        (
                            line_number,
                            payload.get("name", "<missing>"),
                            payload.get("arguments", ""),
                        )
                    )
                elif payload_type == "function_call_output":
                    function_outputs[payload.get("call_id", "")] = (
                        line_number,
                        payload.get("output", ""),
                    )
                elif payload_type == "agent_message":
                    agent_messages.append(
                        (line_number, payload.get("message", ""))
                    )

    print(f"TRACE_LINE_COUNT {trace_lines}")
    print(f"TRACE_MALFORMED_COUNT {len(malformed)}")
    for problem in malformed:
        print(f"TRACE_MALFORMED {problem}")
    print(f"TRACE_OUTER_TYPES {dict(sorted(outer_types.items(), key=str))}")
    print(
        "TRACE_PAYLOAD_TYPES "
        f"{dict(sorted(payload_types.items(), key=str))}"
    )
    print(f"TRACE_FUNCTION_CALL_COUNT {len(function_calls)}")
    for number, name, arguments in function_calls:
        print(f"TRACE_CALL line={number} name={name}")
        print(clipped(arguments))
    print(f"TRACE_FUNCTION_OUTPUT_COUNT {len(function_outputs)}")
    for call_id, (number, output) in sorted(
        function_outputs.items(), key=lambda item: item[1][0]
    ):
        print(f"TRACE_OUTPUT line={number} call_id={call_id}")
        print(clipped(output, 900))
    print(f"TRACE_AGENT_MESSAGE_COUNT {len(agent_messages)}")
    for number, message in agent_messages:
        print(f"TRACE_AGENT_MESSAGE line={number}")
        print(message)

    output_path = ROOT / "codex-output.log"
    output_bytes = output_path.read_bytes()
    output_text = output_bytes.decode("utf-8", errors="replace")
    output_lines = output_text.splitlines()
    print(
        f"CODEX_OUTPUT_READ bytes={len(output_bytes)} "
        f"lines={len(output_lines)} sha256={sha256_file(output_path)}"
    )
    for needle in (
        "#Top",
        "WarnStuckClaimState",
        "kprove",
        "kompile",
        "PROOF.md",
        "VALIDATED",
        "SOUND-BUT-LIMITED",
        "FORMALLY-SOUND-UNVALIDATED",
        "Incomplete work",
        "RESULT:",
    ):
        print(f"CODEX_OUTPUT_COUNT {needle!r}={output_text.count(needle)}")
    print("CODEX_OUTPUT_FIRST_25_LINES")
    print("\n".join(output_lines[:25]))
    print("CODEX_OUTPUT_LAST_50_LINES")
    print("\n".join(output_lines[-50:]))

    for path in (ROOT / "codex-last.txt", ROOT / "prompt.txt"):
        data = path.read_text()
        print(
            f"TEXT_RECORD {path} bytes={len(data.encode())} "
            f"sha256={sha256_file(path)}"
        )
        print(data)

    print(f"EVIDENCE_HASH_FAILURE_COUNT {len(evidence_failures)}")
    return 1 if evidence_failures or malformed else 0


if __name__ == "__main__":
    raise SystemExit(main())
