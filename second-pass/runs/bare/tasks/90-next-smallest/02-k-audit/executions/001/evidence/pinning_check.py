#!/usr/bin/env python3
"""Check that the spec's starting <k> term is the submitted .mpy program."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: pinning_check.py SOLUTION.mpy SPEC.k", file=sys.stderr)
        return 2
    program_path, spec_path = map(Path, sys.argv[1:])
    program = program_path.read_text(encoding="utf-8").strip()
    spec = spec_path.read_text(encoding="utf-8")
    match = re.search(r"<k>\s*(Module\(.*?)\s*=>\s*\.K\s*</k>", spec, re.DOTALL)
    if not match:
        print("could not extract starting <k> program", file=sys.stderr)
        return 2
    claimed_program = match.group(1)
    compact_program = compact(program)
    compact_claim = compact(claimed_program)
    print(f"program_compact_sha256={hashlib.sha256(compact_program.encode()).hexdigest()}")
    print(f"claim_compact_sha256={hashlib.sha256(compact_claim.encode()).hexdigest()}")
    print(f"program_term_byte_length={len(program.encode())}")
    print(f"claim_program_text_byte_length={len(claimed_program.encode())}")
    print(f"structurally_identical_ignoring_layout={compact_program == compact_claim}")
    return 0 if compact_program == compact_claim else 1


if __name__ == "__main__":
    raise SystemExit(main())
