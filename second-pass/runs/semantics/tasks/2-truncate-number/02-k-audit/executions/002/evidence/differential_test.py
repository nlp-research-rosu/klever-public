#!/usr/bin/env python3
"""Independent candidate/canonical differential test for HumanEval/2."""

from __future__ import annotations

import importlib.util
import math
import random
import struct
from pathlib import Path


def load_entry(path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.truncate_number


canonical = load_entry("/reference/canonical.py", "trusted_canonical")
candidate = load_entry("/candidate/solution.py", "candidate_solution")

documented = [3.5]
positive_boundaries = [
    math.nextafter(0.0, math.inf),
    0.25,
    math.nextafter(1.0, 0.0),
    1.0,
    math.nextafter(1.0, math.inf),
    math.nextafter(2.0, 0.0),
    2.0,
    math.nextafter(2.0, math.inf),
    7.75,
    float(2**52),
    math.nextafter(float(2**52), 0.0),
    float(2**53),
    math.nextafter(float.fromhex("0x1.fffffffffffffp+1023"), 0.0),
    float.fromhex("0x1.fffffffffffffp+1023"),
]

rng = random.Random(0x2A71C)
generated = []
while len(generated) < 5000:
    bits = rng.getrandbits(64)
    value = struct.unpack(">d", bits.to_bytes(8, "big"))[0]
    if math.isfinite(value) and value > 0.0:
        generated.append(value)

in_domain = documented + positive_boundaries + generated
mismatches = []
contract_violations = []
for value in in_domain:
    expected = canonical(value)
    actual = candidate(value)
    if actual != expected:
        mismatches.append((value.hex(), expected.hex(), actual.hex()))
    if not (0.0 <= actual < 1.0):
        contract_violations.append((value.hex(), actual.hex()))
    # For positive finite x, math.modf is an implementation-independent
    # decomposition oracle exposed directly by Python's math library.
    frac, integral = math.modf(value)
    if actual != frac:
        contract_violations.append(
            (value.hex(), actual.hex(), f"math.modf={frac.hex()}", integral.hex())
        )

# Zero and negatives are outside the stated positive domain but probe the
# boundary and document that the candidate still agrees with the canonical.
out_of_domain = [0.0, -0.0, -math.nextafter(0.0, math.inf), -0.25, -1.0, -3.5]
out_domain_mismatches = []
for value in out_of_domain:
    expected = canonical(value)
    actual = candidate(value)
    if actual != expected:
        out_domain_mismatches.append((value.hex(), expected.hex(), actual.hex()))

print(f"documented_cases={len(documented)}")
print(f"positive_boundary_cases={len(positive_boundaries)}")
print(f"generated_positive_finite_cases={len(generated)} seed=0x2A71C")
print(f"in_domain_total={len(in_domain)}")
print(f"candidate_canonical_mismatches={len(mismatches)}")
print(f"positive_contract_violations={len(contract_violations)}")
print(f"out_of_domain_boundary_cases={len(out_of_domain)}")
print(f"out_of_domain_candidate_canonical_mismatches={len(out_domain_mismatches)}")
if mismatches:
    print(f"first_mismatch={mismatches[0]}")
if contract_violations:
    print(f"first_contract_violation={contract_violations[0]}")
if out_domain_mismatches:
    print(f"first_out_of_domain_mismatch={out_domain_mismatches[0]}")

if mismatches or contract_violations or out_domain_mismatches:
    raise SystemExit(1)
