#!/usr/bin/env python3
"""Bounded, full-file scan of untrusted candidate generation records."""

from __future__ import annotations

import collections
import hashlib
import json
import pathlib
import re


LOG = pathlib.Path("/candidate/codex-output.log")
TRACE_ROOT = pathlib.Path("/candidate/codex-trace")
PATTERN = re.compile(
    r"#Top|kprove|kompile|krun|WarnStuck|RESULT:|semantic\.k|"
    r"verification\.k|spec\.k|vacu|error|fail",
    re.IGNORECASE,
)
MAX_MATCHES = 80
MAX_TEXT = 500


def bounded(text: str) -> str:
    text = text.replace("\n", "\\n")
    return text if len(text) <= MAX_TEXT else text[:MAX_TEXT] + "...[truncated]"


def scan_log() -> None:
    raw = LOG.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    lines = text.splitlines()
    matches = [(n, line) for n, line in enumerate(lines, 1) if PATTERN.search(line)]
    print("CODEX_OUTPUT")
    print(f"path={LOG}")
    print(f"bytes={len(raw)} lines={len(lines)} sha256={hashlib.sha256(raw).hexdigest()}")
    print(f"matching_lines={len(matches)} shown={min(MAX_MATCHES, len(matches))}")
    for n, line in matches[:MAX_MATCHES]:
        print(f"{n}: {bounded(line)}")
    print("first_lines")
    for n, line in enumerate(lines[:12], 1):
        print(f"{n}: {bounded(line)}")
    print("last_lines")
    start = max(1, len(lines) - 11)
    for n, line in enumerate(lines[-12:], start):
        print(f"{n}: {bounded(line)}")


def scan_trace(path: pathlib.Path) -> None:
    raw = path.read_bytes()
    lines = raw.decode("utf-8", errors="replace").splitlines()
    top_types: collections.Counter[str | None] = collections.Counter()
    payload_types: collections.Counter[str | None] = collections.Counter()
    malformed = 0
    selected: list[tuple[int, str]] = []
    for n, line in enumerate(lines, 1):
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            malformed += 1
            continue
        top_types[obj.get("type")] += 1
        payload = obj.get("payload")
        if isinstance(payload, dict):
            payload_types[payload.get("type")] += 1
        if PATTERN.search(line) and len(selected) < MAX_MATCHES:
            selected.append((n, line))
    print("STRUCTURED_TRACE")
    print(f"path={path}")
    print(f"bytes={len(raw)} lines={len(lines)} sha256={hashlib.sha256(raw).hexdigest()}")
    print(f"malformed={malformed}")
    print(f"top_types={dict(top_types)}")
    print(f"payload_types={dict(payload_types)}")
    print(f"selected_shown={len(selected)}")
    for n, line in selected:
        print(f"{n}: {bounded(line)}")


def main() -> None:
    scan_log()
    traces = sorted(TRACE_ROOT.rglob("*.jsonl"))
    print(f"trace_count={len(traces)}")
    for path in traces:
        scan_trace(path)


if __name__ == "__main__":
    main()
