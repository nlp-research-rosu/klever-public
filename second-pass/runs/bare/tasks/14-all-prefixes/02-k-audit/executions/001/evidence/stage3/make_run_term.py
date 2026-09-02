#!/usr/bin/env python3
"""Wrap a trusted-regenerated Module(...) term in Run(..., all_prefixes(ARG))."""

from __future__ import annotations

import json
import pathlib
import sys


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} SOLUTION.mpy INPUT_STRING", file=sys.stderr)
        return 64
    program = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8").strip()
    argument = json.dumps(sys.argv[2], ensure_ascii=False)
    print("Run(")
    print("  " + program.replace("\n", "\n  ") + ",")
    print(f'  Call(Name("all_prefixes"), Str({argument})))')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
