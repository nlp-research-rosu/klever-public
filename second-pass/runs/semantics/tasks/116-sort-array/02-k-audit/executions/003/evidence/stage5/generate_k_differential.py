#!/usr/bin/env python3
"""Generate deterministic K-concrete assertions from the trusted CPython oracle."""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path


def load_entry(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_array


canonical = load_entry(
    Path("/tmp/audit-work/reconstruction/canonical.py"), "trusted_canonical_for_k"
)
generated = load_entry(
    Path("/tmp/audit-work/reconstruction/solution.py"), "generated_solution_for_k"
)

cases: list[list[int]] = [
    [],
    [0],
    [0, 1],
    [1, 5, 2, 3, 4],
    [1, 0, 2, 3, 4],
    [7, 7, 0, 3, 3, 8, 8, 1],
    [12, 10, 9, 6, 5, 3],
    [0, 1, 2, 3, 4, 7, 8, 15, 16, 31, 32, 63, 64],
    [(1 << 64) - 1, 1 << 64, 3],
]
for values in itertools.product(range(6), repeat=2):
    cases.append(list(values))

rng = random.Random(116_5)
for _ in range(40):
    cases.append([rng.randrange(0, 1 << 32) for _ in range(rng.randrange(0, 20))])

lines = [
    "def sort_array(arr):",
    "    return sorted(",
    "        sorted(arr),",
    "        key=lambda value: (",
    "            0",
    "            if value < 0",
    '            else bin(value).count("1")',
    "        ),",
    "    )",
    "",
]

for values in cases:
    expected = canonical(list(values))
    assert generated(list(values)) == expected
    lines.append(f"assert sort_array({values!r}) == {expected!r}")

output = Path(sys.argv[1])
output.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"GENERATED_CASES {len(cases)}")
print(f"OUTPUT {output}")
