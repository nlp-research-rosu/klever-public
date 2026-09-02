#!/usr/bin/env python3
"""Independent CPython differential test for HumanEval/100."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import random


def load_module(name: str, path: Path):
    spec = spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SCRATCH = Path("/tmp/audit-work/reconstruction")
canonical = load_module("trusted_canonical", SCRATCH / "canonical.py")
candidate = load_module("candidate_solution", SCRATCH / "solution.py")

# n=3 is the documented example. Non-positive values probe the empty-result
# boundary even though the source contract restricts n to positive integers.
explicit = [-10, -3, -1, 0, 1, 2, 3, 4, 5, 10, 100, 1000]
rng = random.Random(100_20260729)
generated = [rng.randint(1, 10_000) for _ in range(1000)]
inputs = explicit + generated

mismatches = []
for n in inputs:
    expected = canonical.make_a_pile(n)
    actual = candidate.make_a_pile(n)
    if actual != expected:
        mismatches.append((n, expected, actual))

print(f"explicit_inputs={explicit}")
print("generated_input_seed=10020260729")
print("generated_input_count=1000")
print("generated_input_range=[1,10000]")
print(f"total_cases={len(inputs)}")
for n in explicit:
    expected = canonical.make_a_pile(n)
    actual = candidate.make_a_pile(n)
    if len(expected) <= 12:
        print(f"case n={n}: canonical={expected!r} candidate={actual!r}")
    else:
        print(
            f"case n={n}: lengths=({len(expected)},{len(actual)}) "
            f"canonical_head_tail={expected[:3]!r}...{expected[-3:]!r} "
            f"candidate_head_tail={actual[:3]!r}...{actual[-3:]!r}"
        )
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"mismatch={mismatch!r}")
assert not mismatches
print("DIFFERENTIAL_TEST=PASS")
