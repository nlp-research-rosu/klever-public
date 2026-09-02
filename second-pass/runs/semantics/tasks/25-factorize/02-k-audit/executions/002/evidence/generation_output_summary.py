#!/usr/bin/env python3
"""Read the complete untrusted Codex output log and report bounded salient lines."""

from __future__ import annotations

import collections
import hashlib
import re
from pathlib import Path


PATH = Path("/generation-evidence/codex-output.log")
PATTERNS = {
    "top": re.compile(r"#Top"),
    "kprove": re.compile(r"\bkprove\b", re.IGNORECASE),
    "kompile": re.compile(r"\bkompile\b", re.IGNORECASE),
    "krun": re.compile(r"\bkrun\b", re.IGNORECASE),
    "warning": re.compile(r"\bwarn(?:ing)?\b", re.IGNORECASE),
    "error": re.compile(r"\berror\b", re.IGNORECASE),
    "failed": re.compile(r"\b(?:fail|failed|failure)\b", re.IGNORECASE),
    "result_marker": re.compile(r"RESULT:\s*(?:KPROVE_PASSED|PARTIAL|BLOCKED)"),
}


def clean(line: str, limit: int = 1000) -> str:
    line = re.sub(r"\x1b\[[0-9;?]*[ -/]*[@-~]", "", line.rstrip("\n\r"))
    return line if len(line) <= limit else line[:limit] + f"...[truncated {len(line) - limit} chars]"


def main() -> int:
    digest = hashlib.sha256(PATH.read_bytes()).hexdigest()
    counts: collections.Counter[str] = collections.Counter()
    selected: list[tuple[int, tuple[str, ...], str]] = []
    first: list[str] = []
    tail: collections.deque[str] = collections.deque(maxlen=20)
    with PATH.open(encoding="utf-8", errors="replace") as stream:
        for number, line in enumerate(stream, 1):
            if number <= 20:
                first.append(clean(line))
            tail.append(clean(line))
            hits = tuple(name for name, pattern in PATTERNS.items() if pattern.search(line))
            for hit in hits:
                counts[hit] += 1
            if hits and (
                "top" in hits
                or "result_marker" in hits
                or "error" in hits
                or "failed" in hits
                or (("kprove" in hits or "kompile" in hits or "krun" in hits) and len(selected) < 250)
            ):
                selected.append((number, hits, clean(line)))
    print(f"path={PATH}")
    print(f"sha256={digest}")
    print(f"line_count={number}")
    print(f"pattern_counts={dict(counts)}")
    print("first_20_lines:")
    for index, line in enumerate(first, 1):
        print(f"  {index}: {line}")
    print("salient_lines:")
    for number, hits, line in selected[-300:]:
        print(f"  {number} [{','.join(hits)}] {line}")
    print("last_20_lines:")
    for line in tail:
        print(f"  {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
