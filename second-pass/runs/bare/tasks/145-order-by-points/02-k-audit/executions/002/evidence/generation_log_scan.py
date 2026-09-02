#!/usr/bin/env python3
"""Scan every line of the untrusted Codex text log and emit a bounded ledger."""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path


LOG = Path("/generation-evidence/codex-output.log")
ANSI = re.compile(r"\x1b(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
INTERESTING = re.compile(
    r"(^exec$|^apply_patch$|^codex$|^user$|^RESULT:|#Top|"
    r"failed in|succeeded in|exited|Exit code|\[Error\]|Warning \()"
)


def main() -> int:
    raw = LOG.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    text = raw.decode("utf-8", errors="replace")
    counts = Counter()
    selected: list[tuple[int, str]] = []
    for number, line in enumerate(text.splitlines(), 1):
        clean = ANSI.sub("", line)
        if clean in {"exec", "apply_patch", "codex", "user"}:
            counts[clean] += 1
        if "#Top" in clean:
            counts["#Top-lines"] += 1
        if "[Error]" in clean:
            counts["error-lines"] += 1
        if INTERESTING.search(clean):
            selected.append((number, clean[:600]))
    print(f"bytes={len(raw)}")
    print(f"lines={len(text.splitlines())}")
    print(f"sha256={digest}")
    print(f"event_counts={dict(sorted(counts.items()))}")
    print(f"selected_line_count={len(selected)}")
    for number, line in selected:
        print(f"{number}: {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
