#!/usr/bin/env python3
"""Check that solutionProgram expands to the exact trusted-regenerated .mpy term."""

from __future__ import annotations

import hashlib
import pathlib
import sys


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    if len(sys.argv) != 3:
        print(
            f"usage: {sys.argv[0]} TRUSTED_REGENERATED.mpy SOLUTION-PROGRAM.k",
            file=sys.stderr,
        )
        return 64

    mpy_path = pathlib.Path(sys.argv[1])
    helper_path = pathlib.Path(sys.argv[2])
    term = mpy_path.read_text(encoding="utf-8").strip()
    indented = "\n".join("    " + line for line in term.splitlines())
    expected = (
        "module SOLUTION-PROGRAM\n"
        "  imports MPY\n"
        '  syntax Program ::= "solutionProgram" [function]\n'
        "  rule solutionProgram =>\n"
        f"{indented}\n"
        "endmodule\n"
    ).encode("utf-8")
    actual = helper_path.read_bytes()
    print(f"TRUSTED_TRANSLATED_TERM: {mpy_path}")
    print(f"SUBMITTED_HELPER: {helper_path}")
    print(f"EXPECTED_SHA256: {digest(expected)}")
    print(f"ACTUAL_SHA256: {digest(actual)}")
    print(f"BYTE_IDENTICAL: {expected == actual}")
    if expected != actual:
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
