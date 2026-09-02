#!/usr/bin/env python3
"""Remove only candidate verification.k lines 6-59 (the five branch bridges)."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: remove_branch_bridges.py INPUT OUTPUT", file=sys.stderr)
        return 64
    source = Path(sys.argv[1]).read_text(encoding="utf-8").splitlines(keepends=True)
    if not any('scope("$proofPath" |-> 1' in line for line in source):
        raise RuntimeError("expected branch bridge marker is absent")
    retained = source[:5] + source[59:]
    Path(sys.argv[2]).write_text("".join(retained), encoding="utf-8")
    print(f"INPUT_LINES: {len(source)}")
    print(f"REMOVED_LINES_1_BASED: 6-59")
    print(f"OUTPUT_LINES: {len(retained)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
