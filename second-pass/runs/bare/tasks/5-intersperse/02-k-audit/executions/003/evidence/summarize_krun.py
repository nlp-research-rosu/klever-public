#!/usr/bin/env python3
"""Emit a bounded summary of a concrete final VList configuration."""

from __future__ import annotations

import hashlib
import json
import re
import sys


def main() -> int:
    text = sys.stdin.read()
    match = re.search(r"VList\s*\(\s*\[(.*?)\.Ints\s*\]\s*\)", text, re.S)
    if match is None:
        print(f"PARSE_FAILURE bytes={len(text.encode())}")
        print(text[:2000])
        return 2
    body = match.group(1).strip()
    if body.endswith(","):
        body = body[:-1]
    values = [] if not body else [int(token.strip()) for token in body.split(",")]
    encoded = json.dumps(values, separators=(",", ":")).encode()
    print(f"RAW_BYTES {len(text.encode())}")
    print(f"RESULT_LENGTH {len(values)}")
    print(f"RESULT_FIRST {values[:6]}")
    print(f"RESULT_LAST {values[-6:]}")
    print(f"RESULT_SHA256 {hashlib.sha256(encoded).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
