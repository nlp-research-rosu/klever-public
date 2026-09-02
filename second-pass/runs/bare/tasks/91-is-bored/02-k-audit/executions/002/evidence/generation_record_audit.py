#!/usr/bin/env python3
"""Parse and summarize every record required by legacy-selected-stage1."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


ROOT = Path("/generation-evidence")
TRACE = (
    ROOT
    / "codex-trace/2026/07/22/"
    "rollout-2026-07-22T06-04-20-019f897f-78ae-75b2-b2be-2505838c95bf.jsonl"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bounded(value: str, limit: int = 700) -> str:
    value = value.replace("\n", "\\n")
    if len(value) <= limit:
        return value
    half = limit // 2
    return value[:half] + "...<bounded>..." + value[-half:]


def main() -> None:
    required = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        ROOT / "invocation.json",
        ROOT / "metrics.json",
        ROOT / "codex-last.txt",
        ROOT / "codex-output.log",
        ROOT / "prompt.txt",
        TRACE,
    ]
    if (ROOT / "usage.json").exists():
        required.append(ROOT / "usage.json")

    for path in required:
        data = path.read_bytes()
        print(
            f"record={path} bytes={len(data)} lines={data.count(bytes([10]))} "
            f"sha256={hashlib.sha256(data).hexdigest()}"
        )

    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads((ROOT / "invocation.json").read_text())
    for name, expected in result["outputs"]["evidence"].items():
        path = ROOT / name
        actual = digest(path)
        print(
            f"stage1_evidence_hash name={name} expected={expected} "
            f"actual={actual} match={actual == expected}"
        )
        if actual != expected:
            raise AssertionError(name)
    for name, expected in invocation["outputs"]["evidence"].items():
        path = ROOT / name
        actual = digest(path)
        if actual != expected:
            raise AssertionError(f"invocation evidence mismatch: {name}")

    rows = [json.loads(line) for line in TRACE.read_text().splitlines()]
    top_types = collections.Counter(row.get("type") for row in rows)
    payload_types = collections.Counter(
        row.get("payload", {}).get("type") for row in rows
    )
    print(f"trace_rows={len(rows)}")
    print(f"trace_top_types={dict(top_types)}")
    print(f"trace_payload_types={dict(payload_types)}")

    call_number = 0
    for line_number, row in enumerate(rows, 1):
        payload = row.get("payload", {})
        if payload.get("type") in {"custom_tool_call", "function_call"}:
            call_number += 1
            content = (
                payload.get("input")
                or payload.get("arguments")
                or payload.get("name")
                or ""
            )
            print(
                f"trace_call={call_number} line={line_number} "
                f"type={payload.get('type')} name={payload.get('name')} "
                f"content={bounded(str(content))}"
            )

    log = (ROOT / "codex-output.log").read_text(errors="replace")
    needles = [
        "kprove",
        "#Top",
        "WarnStuckClaimState",
        "universal-spec",
        "differential cases",
        "RESULT:",
    ]
    for needle in needles:
        matching = [
            (index, line)
            for index, line in enumerate(log.splitlines(), 1)
            if needle in line
        ]
        print(f"log_needle={needle!r} matches={len(matching)}")
        for index, line in matching[:20]:
            print(f"  line={index} text={bounded(line, 500)}")

    final_messages = [
        row["payload"].get("message")
        for row in rows
        if row.get("payload", {}).get("type") == "agent_message"
        and row["payload"].get("phase") == "final_answer"
    ]
    print(f"final_messages={len(final_messages)}")
    for message in final_messages:
        print(f"final_message={bounded(message or '', 1200)}")


if __name__ == "__main__":
    main()
