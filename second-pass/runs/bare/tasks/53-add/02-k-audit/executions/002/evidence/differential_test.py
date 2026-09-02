#!/usr/bin/env python3
"""Independent differential check of trusted canonical vs scratch solution."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import random
import sys


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    canonical = load_module(
        "trusted_canonical", Path("/tmp/audit-work/53-add-audit-002/canonical.py")
    )
    generated = load_module(
        "generated_solution", Path("/tmp/audit-work/53-add-audit-002/solution.py")
    )

    documented = [(2, 3, 5), (5, 7, 12)]
    boundary_pairs = [
        (0, 0),
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0),
        (1, -1),
        (-1, 1),
        (-1, -1),
        (sys.maxsize, 1),
        (-sys.maxsize - 1, -1),
        (2**1024, -(2**1024)),
        (2**4096, 2**4096),
    ]
    grid_values = [-1000, -17, -2, -1, 0, 1, 2, 17, 1000]
    pairs = list(boundary_pairs)
    pairs.extend((x, y) for x in grid_values for y in grid_values)

    rng = random.Random(53002)
    for _ in range(5000):
        bits_x = rng.randrange(0, 1025)
        bits_y = rng.randrange(0, 1025)
        x = rng.getrandbits(bits_x)
        y = rng.getrandbits(bits_y)
        if rng.randrange(2):
            x = -x
        if rng.randrange(2):
            y = -y
        pairs.append((x, y))

    mismatches = []
    for x, y, expected in documented:
        c = canonical.add(x, y)
        g = generated.add(x, y)
        if c != expected or g != expected:
            mismatches.append((x, y, expected, c, g))
    for x, y in pairs:
        c = canonical.add(x, y)
        g = generated.add(x, y)
        if c != g:
            mismatches.append((x, y, c, g))

    print(f"documented_examples={len(documented)}")
    print(f"boundary_and_generated_pairs={len(pairs)}")
    print("conditional_branch_boundaries=0 (straight-line function)")
    print("empty_input_case=not_applicable (contract has two integer arguments)")
    print(f"mismatches={len(mismatches)}")
    if mismatches:
        print(f"first_mismatch={mismatches[0]}")
        return 1
    print("DIFFERENTIAL_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
