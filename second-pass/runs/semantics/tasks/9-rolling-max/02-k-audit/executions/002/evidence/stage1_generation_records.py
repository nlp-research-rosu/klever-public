#!/usr/bin/env python3
"""Parse every selected-stage generation record as untrusted provenance evidence."""

from __future__ import annotations

import collections
import hashlib
import json
import re
from pathlib import Path


ROOT = Path("/generation-evidence")
TRACE_ROOT = ROOT / "codex-trace"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def clipped(text: object, limit: int = 500) -> str:
    if not isinstance(text, str):
        text = json.dumps(text, sort_keys=True)
    text = text.replace("\x1b", "<ESC>")
    if len(text) <= limit:
        return text
    return text[: limit // 2] + f"\n...[{len(text) - limit} chars omitted]...\n" + text[-limit // 2 :]


def main() -> int:
    json_records = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        ROOT / "invocation.json",
        ROOT / "metrics.json",
        ROOT / "usage.json",
    ]
    print("JSON RECORDS")
    for path in json_records:
        parsed = json.loads(path.read_text())
        print(path, "valid-json", type(parsed).__name__, "sha256", sha256(path), "bytes", path.stat().st_size)

    invocation = json.loads((ROOT / "invocation.json").read_text())
    usage = json.loads((ROOT / "usage.json").read_text())
    trace_files = sorted(path for path in TRACE_ROOT.rglob("*") if path.is_file())
    expected_trace_entries = invocation["outputs"]["evidence"]

    print("\nTRACE PARSE")
    all_lines = 0
    outer_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[tuple[str, str]] = collections.Counter()
    response_types: collections.Counter[tuple[str, str, str]] = collections.Counter()
    calls: dict[str, dict] = {}
    outputs: dict[str, dict] = {}
    first_timestamp = None
    last_timestamp = None
    selected_usage_found = False
    final_messages: list[str] = []
    prompt_messages: list[str] = []

    for trace_path in trace_files:
        rel = trace_path.relative_to(ROOT).as_posix()
        actual_hash = sha256(trace_path)
        expected_hash = expected_trace_entries.get(rel)
        print(
            "trace-file",
            rel,
            "sha256",
            actual_hash,
            "expected",
            expected_hash,
            "match",
            actual_hash == expected_hash,
        )
        with trace_path.open() as stream:
            for line_number, line in enumerate(stream, 1):
                record = json.loads(line)
                all_lines += 1
                timestamp = record.get("timestamp")
                first_timestamp = first_timestamp or timestamp
                last_timestamp = timestamp
                outer = record.get("type", "<missing>")
                payload = record.get("payload", {})
                inner = payload.get("type", "<none>")
                outer_types[outer] += 1
                payload_types[(outer, inner)] += 1
                if (
                    trace_path.relative_to(TRACE_ROOT).as_posix()
                    == usage["selected_event"]["relative_path"]
                    and line_number == usage["selected_event"]["line_number"]
                ):
                    selected_usage_found = True
                if outer == "response_item":
                    response_types[
                        (
                            inner,
                            payload.get("name", "<none>"),
                            payload.get("role", "<none>"),
                        )
                    ] += 1
                    if inner == "custom_tool_call":
                        calls[payload["call_id"]] = payload
                    elif inner == "custom_tool_call_output":
                        outputs[payload["call_id"]] = payload
                    elif inner == "message":
                        text = "\n".join(
                            part.get("text", "")
                            for part in payload.get("content", [])
                            if isinstance(part, dict)
                        )
                        if payload.get("role") == "user":
                            prompt_messages.append(text)
                        if payload.get("role") == "assistant":
                            final_messages.append(text)

    print("all_jsonl_lines", all_lines)
    print("first_timestamp", first_timestamp)
    print("last_timestamp", last_timestamp)
    print("outer_types", dict(sorted(outer_types.items())))
    print("payload_types", {str(k): v for k, v in sorted(payload_types.items())})
    print("response_types", {str(k): v for k, v in sorted(response_types.items())})
    print("selected_usage_event_found", selected_usage_found)
    print("tool_call_count", len(calls))
    print("tool_output_count", len(outputs))
    print("unpaired_calls", sorted(set(calls) - set(outputs)))
    print("unpaired_outputs", sorted(set(outputs) - set(calls)))

    print("\nORDERED TOOL CALLS")
    for index, (call_id, payload) in enumerate(calls.items(), 1):
        tool_input = payload.get("input", "")
        output = outputs.get(call_id, {}).get("output", "<missing output>")
        print(f"CALL {index} id={call_id} name={payload.get('name')} status={payload.get('status')}")
        print("INPUT", clipped(tool_input, 800))
        print("OUTPUT", clipped(output, 1000))

    print("\nUSER MESSAGE HASHES")
    for index, message in enumerate(prompt_messages, 1):
        digest = hashlib.sha256(message.encode()).hexdigest()
        print(index, "chars", len(message), "sha256", digest, "head", clipped(message, 300))

    print("\nASSISTANT MESSAGE SUMMARIES")
    for index, message in enumerate(final_messages, 1):
        print(index, clipped(message, 700))

    print("\nTEXT RECORD SCAN")
    for path in [ROOT / "prompt.txt", ROOT / "codex-last.txt", ROOT / "codex-output.log"]:
        text = path.read_text(errors="replace")
        lines = text.splitlines()
        print(
            path,
            "sha256",
            sha256(path),
            "bytes",
            path.stat().st_size,
            "lines",
            len(lines),
            "nul_count",
            text.count("\x00"),
        )
        marker_counts = {
            marker: len(re.findall(re.escape(marker), text))
            for marker in [
                "RESULT: KPROVE_PASSED",
                "#Top",
                "WarnStuckClaimState",
                "timed out",
                "failed in",
                " exited ",
            ]
        }
        print("marker_counts", marker_counts)
        print("head", clipped("\n".join(lines[:12]), 1000))
        print("tail", clipped("\n".join(lines[-20:]), 1400))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
