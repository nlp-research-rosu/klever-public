#!/usr/bin/env python3
"""Bounded structural summary of the untrusted generation trace."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path


TRACE = Path(
    "/candidate/codex-trace/2026/07/22/"
    "rollout-2026-07-22T07-14-01-019f89bf-45c7-76b1-ac86-14068b746967.jsonl"
)


def main() -> None:
    rows = [json.loads(line) for line in TRACE.read_text().splitlines()]
    print(f"trace={TRACE}")
    print(f"lines={len(rows)}")
    print("top_types=" + repr(Counter(row.get("type") for row in rows)))
    print(
        "response_payload_types="
        + repr(
            Counter(
                row.get("payload", {}).get("type")
                for row in rows
                if row.get("type") == "response_item"
            )
        )
    )
    print("claimed_shell_commands:")
    for index, row in enumerate(rows, 1):
        payload = row.get("payload", {})
        if (
            row.get("type") == "response_item"
            and payload.get("type") == "custom_tool_call"
            and payload.get("name") == "exec"
        ):
            source = str(payload.get("input", payload.get("arguments", "")))
            if "exec_command" in source:
                print(f"line={index} {source[:1200]}")


if __name__ == "__main__":
    main()
