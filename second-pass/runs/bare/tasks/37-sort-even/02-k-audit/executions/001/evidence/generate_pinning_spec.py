#!/usr/bin/env python3
"""Wrap a trusted-translator .mpy term in a K equality/reachability claim."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mpy", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--module", default="PINNING-SPEC")
    parser.add_argument("--label", default="program-term-pinning")
    args = parser.parse_args()
    term = args.mpy.read_text(encoding="utf-8").strip()
    rendered = (
        'requires "verification.k"\n\n'
        f"module {args.module}\n"
        "  imports VERIFICATION\n\n"
        "  claim solutionProgram()\n"
        f"    => {term}\n"
        f"    [label({args.label})]\n"
        "endmodule\n"
    )
    args.output.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
