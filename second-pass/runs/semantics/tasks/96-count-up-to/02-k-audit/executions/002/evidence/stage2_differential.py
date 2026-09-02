#!/usr/bin/env python3
"""Independent differential test of the trusted and generated Python entries."""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.count_up_to


canonical = load_entry("trusted_count_up_to", Path("/reference/canonical.py"))
generated = load_entry("generated_count_up_to", Path("/candidate/solution.py"))

documented = {
    5: [2, 3],
    11: [2, 3, 5, 7],
    0: [],
    20: [2, 3, 5, 7, 11, 13, 17, 19],
    1: [],
    18: [2, 3, 5, 7, 11, 13, 17],
}

# 0..500 exhausts the empty/outer-loop boundary, the zero-iteration and
# one-iteration divisor scans, both is_prime branches, prime and composite
# bounds, squares, and many repetitions of all control-flow paths.
inputs = list(range(0, 501))
inputs += [503, 509, 510, 511, 512, 997, 998, 999, 1000, 1024, 2048, 5000]
rng = random.Random(960026)
generated_inputs = [rng.randrange(0, 2501) for _ in range(200)]
inputs += generated_inputs
inputs = list(dict.fromkeys(inputs))

print("contract_domain=non-negative Python integers")
print(f"documented_examples={json.dumps(documented, sort_keys=True)}")
print("exhaustive_inputs=0..500")
print(
    "selected_boundaries="
    + json.dumps([503, 509, 510, 511, 512, 997, 998, 999, 1000, 1024, 2048, 5000])
)
print("random_seed=960026")
print("generated_inputs=" + json.dumps(generated_inputs))
print(f"unique_input_count={len(inputs)}")

mismatches = []
for n in inputs:
    expected = canonical(n)
    actual = generated(n)
    if n in documented and expected != documented[n]:
        raise AssertionError(
            f"trusted canonical contradicts documented example n={n}: {expected}"
        )
    if actual != expected:
        mismatches.append({"n": n, "canonical": expected, "generated": actual})

for n, expected in sorted(documented.items()):
    actual = generated(n)
    if actual != expected:
        mismatches.append(
            {"n": n, "documented": expected, "generated": actual}
        )

print(f"mismatch_count={len(mismatches)}")
if mismatches:
    print("mismatches=" + json.dumps(mismatches, sort_keys=True))
    raise SystemExit(1)
print("RESULT=PASS")
