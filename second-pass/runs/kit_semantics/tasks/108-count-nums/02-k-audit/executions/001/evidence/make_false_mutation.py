#!/usr/bin/env python3
"""Create a fresh off-by-one mutation of the symbolic entry postcondition."""

from __future__ import annotations

import sys
from pathlib import Path


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"expected exactly one occurrence of {old!r}, found {count}")
    return text.replace(old, new, 1)


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: make_false_mutation.py INPUT-spec.k OUTPUT.k", file=sys.stderr)
        return 2
    source = Path(sys.argv[1])
    output = Path(sys.argv[2])
    text = source.read_text()
    text = replace_once(text, "module SPEC\n", "module AUDIT-SPEC-FALSE\n")
    text = replace_once(
        text,
        "ensures ?RESULT ==Int countNumsSpec(vCons(I, R))",
        "ensures ?RESULT ==Int countNumsSpec(vCons(I, R)) +Int 1",
    )
    output.write_text(text)
    print(f"source={source}")
    print(f"output={output}")
    print("mutation=nonempty entry result must equal the established count plus one")
    print("satisfying_counterexample=[11]: real/canonical result 1, false target 2")
    return 0


if __name__ == "__main__":
    sys.exit(main())
