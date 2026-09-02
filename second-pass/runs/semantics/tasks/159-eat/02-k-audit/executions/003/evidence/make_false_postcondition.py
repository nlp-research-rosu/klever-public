#!/usr/bin/env python3
"""Create a parseable off-by-one mutation of the first positive claim."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {Path(sys.argv[0]).name} SPEC.k OUTPUT.k")
        return 2
    source = Path(sys.argv[1]).read_text(encoding="utf-8")
    source = source.replace("module EAT-SPEC", "module EAT-SPEC-VACUITY", 1)
    old = "NUMBER +Int NEED,"
    new = "NUMBER +Int NEED +Int 1,"
    if source.count(old) != 1:
        raise ValueError(
            f"expected exactly one first-branch result occurrence, got {source.count(old)}"
        )
    mutated = source.replace(old, new, 1)
    Path(sys.argv[2]).write_text(mutated, encoding="utf-8")
    print(f"output={sys.argv[2]}")
    print("mutation=first result component NUMBER+NEED -> NUMBER+NEED+1")
    print("satisfying_witness=(NUMBER,NEED,REMAINING)=(5,6,10)")
    print("actual=[11,4] mutated_postcondition=[12,4]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
