#!/usr/bin/env python3
"""Create a materially wrong source body to test proof body sensitivity."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("output")
    args = parser.parse_args()
    source = Path(args.source).read_text(encoding="utf-8")
    needle = "    balance = 0\n"
    replacement = "    return True\n    balance = 0\n"
    if source.count(needle) != 1:
        raise RuntimeError("expected exactly one initialization line")
    mutated = source.replace(needle, replacement)
    Path(args.output).write_text(mutated, encoding="utf-8")
    print("mutation=insert unconditional return True before original body")
    print("witness_input='('")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
