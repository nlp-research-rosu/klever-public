#!/usr/bin/env python3
"""Read the complete generation stdout/stderr record and print a bounded index."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


PATH = Path("/generation-evidence/codex-output.log")
PATTERNS = {
    "top": re.compile(r"#Top"),
    "kprove": re.compile(r"\bkprove\b"),
    "kompile": re.compile(r"\bkompile\b"),
    "krun": re.compile(r"\bkrun\b"),
    "warn_stuck": re.compile(r"WarnStuckClaimState"),
    "error": re.compile(r"\[Error\]|Traceback|UNEXPECTED"),
    "result": re.compile(r"RESULT:"),
    "validated": re.compile(r"\bVALIDATED\b"),
}


def clipped(line: str, limit: int = 1000) -> str:
    line = line.rstrip("\r\n")
    return line if len(line) <= limit else line[:limit] + "...[truncated]"


def main() -> None:
    data = PATH.read_bytes()
    text = data.decode("utf-8", errors="replace")
    lines = text.splitlines()
    print(f"path={PATH}")
    print(f"bytes={len(data)}")
    print(f"lines={len(lines)}")
    print(f"sha256={hashlib.sha256(data).hexdigest()}")
    print(f"replacement_characters={text.count(chr(0xfffd))}")
    for label, pattern in PATTERNS.items():
        indexes = [index for index, line in enumerate(lines, 1) if pattern.search(line)]
        print(f"pattern_{label}_count={len(indexes)}")
        print(f"pattern_{label}_first_lines={indexes[:30]}")
    print("FIRST_LINES")
    for index, line in enumerate(lines[:20], 1):
        print(f"{index}: {clipped(line)}")
    print("LAST_LINES")
    start = max(1, len(lines) - 19)
    for index, line in enumerate(lines[-20:], start):
        print(f"{index}: {clipped(line)}")
    print("KEY_LINE_SAMPLE")
    emitted = 0
    for index, line in enumerate(lines, 1):
        if any(pattern.search(line) for pattern in PATTERNS.values()):
            print(f"{index}: {clipped(line)}")
            emitted += 1
            if emitted == 300:
                print("KEY_LINE_SAMPLE_TRUNCATED_AT=300")
                break


if __name__ == "__main__":
    main()
