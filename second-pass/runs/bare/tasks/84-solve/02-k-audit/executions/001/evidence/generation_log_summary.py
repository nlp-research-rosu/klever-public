#!/usr/bin/env python3
"""Read the complete untrusted generation logs and emit a bounded claim summary."""

from __future__ import annotations

import hashlib
import pathlib


def summarize(path: pathlib.Path) -> None:
    data = path.read_bytes()
    text = data.decode("utf-8", errors="replace")
    lines = text.splitlines()
    print(f"path={path}")
    print(f"bytes={len(data)} lines={len(lines)} sha256={hashlib.sha256(data).hexdigest()}")
    for marker in (
        "#Top",
        "WarnStuckClaimState",
        "[Error]",
        "exit_code",
        "KPROVE_PASSED",
        "RESULT:",
    ):
        print(f"count[{marker!r}]={text.count(marker)}")
    print("first_12_lines:")
    for line in lines[:12]:
        print(f"  {line}")
    print("last_30_lines:")
    for line in lines[-30:]:
        print(f"  {line}")
    print()


def main() -> int:
    summarize(pathlib.Path("/candidate/codex-last.txt"))
    summarize(pathlib.Path("/candidate/codex-output.log"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
