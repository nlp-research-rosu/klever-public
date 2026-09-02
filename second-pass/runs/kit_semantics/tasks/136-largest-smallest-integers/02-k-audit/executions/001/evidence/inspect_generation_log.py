#!/usr/bin/env python3
"""Read every line of the untrusted generation transcript and summarize markers."""

from __future__ import annotations

import argparse
import collections
from pathlib import Path


MARKERS = (
    "#Top",
    "WarnStuckClaimState",
    "[Error]",
    " succeeded in ",
    " failed in ",
    "timed out",
    "VALIDATED",
    "RESULT: KPROVE_PASSED",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("log", type=Path)
    args = parser.parse_args()

    counts: collections.Counter[str] = collections.Counter()
    line_count = 0
    byte_count = 0
    first_line = None
    last_line = None
    with args.log.open("rb") as stream:
        for raw_line in stream:
            line_count += 1
            byte_count += len(raw_line)
            line = raw_line.decode("utf-8", errors="replace").rstrip("\n")
            first_line = first_line if first_line is not None else line
            last_line = line
            for marker in MARKERS:
                if marker in line:
                    counts[marker] += 1

    print(f"lines={line_count}")
    print(f"bytes={byte_count}")
    print(f"first_line={first_line!r}")
    print(f"last_line={last_line!r}")
    for marker in MARKERS:
        print(f"marker={marker!r} count={counts[marker]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
