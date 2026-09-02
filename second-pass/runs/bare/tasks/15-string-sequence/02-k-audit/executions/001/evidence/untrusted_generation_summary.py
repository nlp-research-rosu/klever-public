#!/usr/bin/env python3
"""Read complete untrusted prose logs and emit bounded claim-focused summaries."""

from __future__ import annotations

import re
import sys
from pathlib import Path


pattern = re.compile(
    r"(RESULT:|KPROVE|#Top|kprove|krun|kompile|semantic|spec\.k|solution\.mpy|proof)",
    re.IGNORECASE,
)

for name in sys.argv[1:]:
    path = Path(name)
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    matching = [(i, line) for i, line in enumerate(lines, 1) if pattern.search(line)]
    print(f"FILE: {path}")
    print(f"bytes={len(text.encode('utf-8'))} lines={len(lines)} matching_lines={len(matching)}")
    for lineno, line in matching[:120]:
        if len(line) > 600:
            line = line[:600] + f"... [truncated {len(line) - 600} characters]"
        print(f"{lineno}: {line}")
    if len(matching) > 120:
        print(f"... [omitted {len(matching) - 120} additional matching lines]")
