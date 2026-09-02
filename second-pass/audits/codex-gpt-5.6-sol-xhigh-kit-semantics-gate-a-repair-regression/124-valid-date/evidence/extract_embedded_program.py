#!/usr/bin/env python3
"""Extract only the RHS term of verification.k's solutionProgram equation."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("verification", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    text = args.verification.read_text(encoding="utf-8")
    begin_marker = "// BEGIN_SOLUTION_MPY"
    end_marker = "// END_SOLUTION_MPY"
    if text.count(begin_marker) != 1 or text.count(end_marker) != 1:
        raise SystemExit("expected exactly one pair of solution markers")
    block = text.split(begin_marker, 1)[1].split(end_marker, 1)[0].strip()
    prefix = "rule solutionProgram =>"
    if not block.startswith(prefix):
        raise SystemExit("marked block does not begin with solutionProgram equation")
    term = block[len(prefix) :].strip()
    if not term.startswith("Module("):
        raise SystemExit("solutionProgram RHS is not a Module term")
    args.output.write_text(term + "\n", encoding="utf-8")
    print(f"extracted_bytes={len((term + chr(10)).encode('utf-8'))}")
    print(f"output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
