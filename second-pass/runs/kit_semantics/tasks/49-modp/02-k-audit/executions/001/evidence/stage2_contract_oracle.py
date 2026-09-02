#!/usr/bin/env python3

"""Check the generated entry point against Python's modular-power primitive."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


solution_path = Path("/tmp/audit-work/49-modp/solution.py")
spec = importlib.util.spec_from_file_location("generated_solution_contract", solution_path)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load {solution_path}")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

cases = [(n, p) for n in range(0, 257) for p in range(-64, 65) if p != 0]
cases += [(0, -1), (0, 1), (1101, 101), (10000, -101), (10000, 101)]
rng = random.Random(149049)
cases += [
    (rng.randint(0, 2000), rng.choice(tuple(range(-256, 0)) + tuple(range(1, 257))))
    for _ in range(4000)
]
cases = sorted(set(cases))

mismatches = []
for n, p in cases:
    expected = pow(2, n, p)
    actual = module.modp(n, p)
    if type(actual) is not int or actual != expected:
        mismatches.append((n, p, expected, type(actual).__name__, actual))

print("oracle=CPython pow(2,n,p)")
print("domain=n>=0 and p!=0")
print("systematic=n 0..256; p -64..64 except 0")
print("random_seed=149049 random_cases=4000")
print(f"distinct_cases={len(cases)}")
print(f"mismatches={len(mismatches)}")
for witness in mismatches[:20]:
    print(f"WITNESS={witness!r}")
raise SystemExit(1 if mismatches else 0)
