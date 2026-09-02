#!/usr/bin/env python3
"""Wrap the regenerated submitted Module term in a K identity claim."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mpy", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    module_term = arguments.mpy.read_text(encoding="utf-8").rstrip()
    indented_term = module_term.replace("\n", "\n         ")
    spec = (
        'requires "verification.k"\n\n'
        "module AUDIT-PROGRAM-IDENTITY\n"
        "  imports VERIFICATION\n\n"
        "  claim [submitted-constructor-identity]:\n"
        "    <k> solutionProgram\n"
        "      => "
        + indented_term
        + " </k>\n"
        "    <env> 0 </env>\n"
        "    <scopes>\n"
        "      0 |-> scope(.Map, parent(-1))\n"
        "      -1 |-> builtinsScope\n"
        "    </scopes>\n"
        "    <scopeLoc> 1 </scopeLoc>\n"
        "    <heap> .Map </heap>\n"
        "    <heapLoc> 0 </heapLoc>\n"
        "    <stack> .List </stack>\n"
        "    <ret> noRet </ret>\n"
        "    <exc> NoExc </exc>\n"
        "    <exit-code> 0 </exit-code>\n"
        "endmodule\n"
    )
    arguments.output.write_text(spec, encoding="utf-8")
    print(f"MPY_BYTES={arguments.mpy.stat().st_size}")
    print(f"SPEC_BYTES={arguments.output.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
