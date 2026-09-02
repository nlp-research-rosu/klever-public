#!/usr/bin/env python3
"""Create a syntactically valid wrong submitted-program mutation for pinning."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    text = args.source.read_text(encoding="utf-8")
    old = "    Return(Bool(true))))\n"
    new = "    Return(Bool(false))))\n"
    if text.count(old) != 1:
        raise RuntimeError(f"expected one final true return, found {text.count(old)}")
    args.output.write_text(text.replace(old, new), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
