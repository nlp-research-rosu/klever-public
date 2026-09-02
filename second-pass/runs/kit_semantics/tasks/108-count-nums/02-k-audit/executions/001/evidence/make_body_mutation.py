#!/usr/bin/env python3
"""Mutate the program term actually executed by the nonempty entry claim."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: make_body_mutation.py INPUT-spec.k OUTPUT.k", file=sys.stderr)
        return 2
    source = Path(sys.argv[1])
    output = Path(sys.argv[2])
    text = source.read_text()
    if text.count("module SPEC\n") != 1:
        raise RuntimeError("unexpected source module")
    text = text.replace("module SPEC\n", "module AUDIT-BODY-FALSE\n", 1)
    needle = 'Assign(Name("count"), Int(0))'
    positions = []
    start = 0
    while True:
        found = text.find(needle, start)
        if found < 0:
            break
        positions.append(found)
        start = found + len(needle)
    if len(positions) != 4:
        raise RuntimeError(f"expected four pinned closure initializers, found {len(positions)}")
    last = positions[-1]
    text = text[:last] + 'Assign(Name("count"), Int(1))' + text[last + len(needle) :]
    output.write_text(text)
    print(f"source={source}")
    print(f"output={output}")
    print("mutation=nonempty entry closure initializes count to 1, target unchanged")
    print("satisfying_counterexample=[11]: mutated result 2, target result 1")
    print(f"mutated_byte_offset={last}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
