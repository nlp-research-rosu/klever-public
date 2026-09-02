#!/usr/bin/env python3
import importlib.util
import random
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.change_base


canonical = load_function("trusted_canonical", Path("/reference/canonical.py"))
generated = load_function(
    "generated_solution", Path("/tmp/audit-work/44-change-base/solution.py")
)

cases = {
    (8, 3),
    (8, 2),
    (7, 2),
    (0, 2),
    (0, 9),
    (-1, 2),
    (-8, 3),
    (1, 2),
    (2, 2),
    (3, 2),
    (8, 9),
    (9, 9),
    (10, 9),
    (2**63 - 1, 2),
    (10**50, 9),
}
for base in range(2, 10):
    for x in range(-64, 513):
        cases.add((x, base))

rng = random.Random(440029)
for _ in range(1000):
    cases.add((rng.randint(-(10**12), 10**12), rng.randint(2, 9)))

mismatches = []
errors = []
for x, base in sorted(cases):
    try:
        expected = canonical(x, base)
    except Exception as err:
        expected = ("EXCEPTION", type(err).__name__, str(err))
    try:
        actual = generated(x, base)
    except Exception as err:
        actual = ("EXCEPTION", type(err).__name__, str(err))
    if actual != expected:
        mismatches.append((x, base, expected, actual))
    if isinstance(expected, tuple) or isinstance(actual, tuple):
        errors.append((x, base, expected, actual))

print("oracle=/reference/canonical.py:change_base")
print("generated=/tmp/audit-work/44-change-base/solution.py:change_base")
print("documented_examples=[(8,3),(8,2),(7,2)]")
print("exhaustive_grid=x=-64..512,base=2..9")
print("random_seed=440029 random_cases=1000 range=[-10^12,10^12],base=2..9")
print(f"unique_cases={len(cases)}")
print(f"errors={len(errors)}")
print(f"mismatches={len(mismatches)}")
print(f"mismatches_x_gt_0={sum(x > 0 for x, _, _, _ in mismatches)}")
print(f"mismatches_x_eq_0={sum(x == 0 for x, _, _, _ in mismatches)}")
print(f"mismatches_x_lt_0={sum(x < 0 for x, _, _, _ in mismatches)}")
for mismatch in mismatches[:40]:
    print(f"MISMATCH {mismatch!r}")
if len(mismatches) > 40:
    print(f"MISMATCHES_OMITTED={len(mismatches) - 40}")
raise SystemExit(1 if mismatches or errors else 0)
