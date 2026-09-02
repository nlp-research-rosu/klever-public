#!/usr/bin/env python3
import hashlib
from pathlib import Path


output_path = Path("/generation-evidence/codex-output.log")
last_path = Path("/generation-evidence/codex-last.txt")
raw = output_path.read_bytes()
text = raw.decode("utf-8", errors="strict")
lines = text.splitlines()
last_text = last_path.read_text()

print(f"bytes={len(raw)}")
print(f"sha256={hashlib.sha256(raw).hexdigest()}")
print(f"utf8_valid=True")
print(f"lines={len(lines)}")
print(f"max_line_length={max(map(len, lines), default=0)}")
for pattern in [
    "#Top",
    "WarnStuckClaimState",
    "RESULT: KPROVE_PASSED",
    "VALIDATED",
    "EXPECTED FAILURE",
    "mismatches: 0",
    "Error",
    "Traceback",
]:
    print(f"pattern={pattern!r} occurrences={text.count(pattern)}")
print(f"codex_last_embedded={last_text.strip() in text}")

print("FIRST_LINES")
for line in lines[:8]:
    print(line[:500])
print("LAST_LINES")
for line in lines[-16:]:
    print(line[:500])
