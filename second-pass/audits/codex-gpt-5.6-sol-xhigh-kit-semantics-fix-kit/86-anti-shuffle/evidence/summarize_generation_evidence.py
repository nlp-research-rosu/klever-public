#!/usr/bin/env python3
"""Summarize untrusted generation records without treating them as authority."""

from __future__ import annotations

import collections
import hashlib
import json
import os
from pathlib import Path


CANDIDATE = Path("/candidate")


def describe_required(name: str) -> None:
    path = CANDIDATE / name
    if not path.exists() and not path.is_symlink():
        print(f"{name}: MISSING")
        return
    metadata = path.lstat()
    print(
        f"{name}: regular={path.is_file()} symlink={path.is_symlink()} "
        f"bytes={metadata.st_size} sha256={hashlib.sha256(path.read_bytes()).hexdigest()}"
    )


def main() -> int:
    required = [
        "run-input.json",
        "metrics.json",
        "codex-last.txt",
        "codex-output.log",
    ]
    for name in required:
        describe_required(name)

    for name in ("run-input.json", "metrics.json"):
        parsed = json.loads((CANDIDATE / name).read_text())
        print(f"{name}: valid_json keys={sorted(parsed)}")
        print(json.dumps(parsed, sort_keys=True))

    last = (CANDIDATE / "codex-last.txt").read_text(errors="replace")
    print(f"codex-last.txt: lines={len(last.splitlines())} final={last.splitlines()[-1]!r}")

    generation_log = (CANDIDATE / "codex-output.log").read_text(errors="replace")
    print(
        "codex-output.log: "
        f"lines={len(generation_log.splitlines())} "
        f"top_mentions={generation_log.count('#Top')} "
        f"kprove_mentions={generation_log.count('kprove')} "
        f"result_markers={generation_log.count('RESULT:')}"
    )

    trace_files = sorted((CANDIDATE / "codex-trace").rglob("*"))
    regular_trace_files = [path for path in trace_files if path.is_file()]
    print(f"structured_trace_files={len(regular_trace_files)}")
    for path in regular_trace_files:
        counts: collections.Counter[str] = collections.Counter()
        valid = 0
        invalid = 0
        for line in path.read_text(errors="replace").splitlines():
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                invalid += 1
                continue
            valid += 1
            counts[str(item.get("type", "<no-type>"))] += 1
        print(
            f"trace={path.relative_to(CANDIDATE)} regular={not path.is_symlink()} "
            f"valid_jsonl={valid} invalid_jsonl={invalid} event_types={dict(sorted(counts.items()))}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
