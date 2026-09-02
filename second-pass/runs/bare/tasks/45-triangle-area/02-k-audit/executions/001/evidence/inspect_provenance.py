#!/usr/bin/env python3
"""Read every JSONL trace record and summarize the untrusted generation record."""

from __future__ import annotations

import collections
import hashlib
import json
import pathlib
import re


TRACE = pathlib.Path(
    "/candidate/codex-trace/2026/07/22/"
    "rollout-2026-07-22T04-56-38-019f8941-7ef9-7792-8750-f0c2d41d7fbc.jsonl"
)
CODEX_OUTPUT = pathlib.Path("/candidate/codex-output.log")


def main() -> None:
    taxonomy: collections.Counter[tuple[str, str, str, str]] = collections.Counter()
    commands: list[str] = []
    outputs: list[str] = []
    records = 0

    with TRACE.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            records += 1
            payload = record.get("payload", {})
            taxonomy[
                (
                    str(record.get("type", "")),
                    str(payload.get("type", "")),
                    str(payload.get("role", "")),
                    str(payload.get("name", "")),
                )
            ] += 1

            if record.get("type") != "response_item":
                continue
            if payload.get("type") in {"function_call", "custom_tool_call"}:
                arguments = payload.get("arguments", payload.get("input", ""))
                commands.append(
                    f"{line_number}: {payload.get('name', '')} {arguments}"
                )
            elif payload.get("type") in {"function_call_output", "custom_tool_call_output"}:
                raw_output = payload.get("output", "")
                if isinstance(raw_output, list):
                    output = "\n".join(
                        str(item.get("text", item))
                        for item in raw_output
                        if isinstance(item, dict)
                    )
                else:
                    output = str(raw_output)
                matched = [
                    row
                    for row in output.splitlines()
                    if re.search(
                        r"(Process exited with code|#Top|WarnStuckClaimState|"
                        r"\[Error\]|timed out|succeeded|failed)",
                        row,
                    )
                ]
                if matched:
                    outputs.append(f"{line_number}: " + " | ".join(matched[:12]))

    print(f"TRACE: {TRACE}")
    print(f"PARSED_RECORDS: {records}")
    print("TAXONOMY:")
    for key, count in sorted(taxonomy.items()):
        print(f"  {count:3d} {key}")
    print("FUNCTION_CALLS:")
    for command in commands:
        print(f"  {command}")
    print("SELECTED_FUNCTION_OUTPUT_STATUS:")
    for output in outputs:
        print(f"  {output}")

    output_bytes = CODEX_OUTPUT.read_bytes()
    output_text = output_bytes.decode("utf-8", errors="replace")
    print("CODEX_OUTPUT_FULL_SCAN:")
    print(f"  path={CODEX_OUTPUT}")
    print(f"  sha256={hashlib.sha256(output_bytes).hexdigest()}")
    print(f"  bytes={len(output_bytes)}")
    print(f"  lines={len(output_text.splitlines())}")
    print(f"  exec_markers={sum(line == 'exec' for line in output_text.splitlines())}")
    print(f"  top_markers={sum(line == '#Top' for line in output_text.splitlines())}")
    print(f"  error_markers={output_text.count('[Error]')}")
    print(f"  stuck_markers={output_text.count('WarnStuckClaimState')}")
    print(
        "  final_result_claim="
        + next(
            (
                line
                for line in reversed(output_text.splitlines())
                if line.startswith("RESULT:")
            ),
            "<absent>",
        )
    )


if __name__ == "__main__":
    main()
