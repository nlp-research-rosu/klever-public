#!/usr/bin/env python3
"""Read the complete untrusted generation text records and report bounded facts."""

from __future__ import annotations

import re
from pathlib import Path


root = Path("/generation-evidence")
for name in ("codex-last.txt", "codex-output.log", "prompt.txt"):
    path = root / name
    text = path.read_text(errors="replace")
    failed_words = len(re.findall(r"\bfailed\b", text, re.IGNORECASE))
    timeout_words = len(re.findall(r"\b(?:timeout|timed out)\b", text, re.IGNORECASE))
    print(f"{name}: bytes={path.stat().st_size} lines={len(text.splitlines())}")
    print(f"  top_markers={text.count('#Top')}")
    print(f"  passed_markers={text.count('KPROVE_PASSED')}")
    print(f"  failed_words={failed_words}")
    print(f"  timeout_words={timeout_words}")

last = (root / "codex-last.txt").read_text(errors="replace")
print("codex-last-content:")
print(last)

output = (root / "codex-output.log").read_text(errors="replace")
salient_patterns = (
    r"^COMMAND:.*$",
    r"^RESULT:.*$",
    r"^Implemented and verified.*$",
    r"^#Top$",
    r"^exhaustive CPython oracle:.*$",
    r"^solution\\.mpy regeneration check:.*$",
)
salient: list[str] = []
for line in output.splitlines():
    if any(re.search(pattern, line) for pattern in salient_patterns):
        salient.append(line)
print("salient_generation_claims:")
for line in salient[-80:]:
    print(" ", line)
