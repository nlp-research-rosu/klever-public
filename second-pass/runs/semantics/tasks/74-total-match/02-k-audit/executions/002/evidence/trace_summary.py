#!/usr/bin/env python3
"""Parse every generation trace record and summarize untrusted generation claims."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")
LOG = Path("/generation-evidence/codex-output.log")


def text_fragments(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from text_fragments(item)
    elif isinstance(value, list):
        for item in value:
            yield from text_fragments(item)


def main() -> None:
    files = sorted(TRACE_ROOT.rglob("*"))
    trace_files = [path for path in files if path.is_file()]
    print(f"TRACE_FILES {len(trace_files)}")
    total = 0
    top_types = collections.Counter()
    payload_types = collections.Counter()
    command_lines: list[str] = []
    result_mentions: list[str] = []
    for path in trace_files:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        print(f"TRACE_FILE {path.relative_to(TRACE_ROOT)} bytes={path.stat().st_size} sha256={digest}")
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                record = json.loads(line)
                total += 1
                top_types[str(record.get("type"))] += 1
                payload = record.get("payload")
                if isinstance(payload, dict):
                    payload_types[str(payload.get("type"))] += 1
                joined = " ".join(text_fragments(record))
                if "/bin/bash -lc" in joined or "exec_command" in joined:
                    command_lines.append(f"{path.name}:{line_number}: {joined[:500]}")
                if "#Top" in joined or "KPROVE_PASSED" in joined or "WarnStuckClaimState" in joined:
                    result_mentions.append(f"{path.name}:{line_number}: {joined[:500]}")
    print(f"TRACE_RECORDS {total}")
    print(f"TOP_LEVEL_TYPES {dict(sorted(top_types.items()))}")
    print(f"PAYLOAD_TYPES {dict(sorted(payload_types.items()))}")
    print(f"COMMAND_RECORDS {len(command_lines)}")
    for item in command_lines:
        print(f"COMMAND {item}")
    print(f"RESULT_MENTION_RECORDS {len(result_mentions)}")
    for item in result_mentions:
        print(f"RESULT_MENTION {item}")

    raw = LOG.read_bytes()
    decoded = raw.decode("utf-8")
    print(
        "CODEX_OUTPUT "
        f"bytes={len(raw)} lines={decoded.count(chr(10))} "
        f"sha256={hashlib.sha256(raw).hexdigest()}"
    )
    markers = {
        "#Top": decoded.count("#Top"),
        "WarnStuckClaimState": decoded.count("WarnStuckClaimState"),
        "KPROVE_PASSED": decoded.count("KPROVE_PASSED"),
        "timeout": decoded.lower().count("timeout"),
    }
    print(f"CODEX_OUTPUT_MARKERS {markers}")
    print("TRACE_PARSE_RESULT OK")


if __name__ == "__main__":
    main()
