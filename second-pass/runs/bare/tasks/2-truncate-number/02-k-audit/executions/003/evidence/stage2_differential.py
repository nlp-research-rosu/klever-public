#!/usr/bin/env python3
"""Independent differential test for HumanEval/2 over positive finite floats."""

from __future__ import annotations

import importlib.util
import math
import random
import struct
from pathlib import Path


def load(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load(Path("/reference/canonical.py"), "trusted_canonical")
candidate = load(Path("/tmp/audit-work/source/solution.py"), "candidate_solution")


def bits(value: float) -> str:
    return struct.pack(">d", value).hex()


explicit = [
    3.5,  # documented example
    math.nextafter(0.0, 1.0),  # least positive subnormal
    float.fromhex("0x0.fffffffffffffp-1022"),  # greatest subnormal
    float.fromhex("0x1.0000000000000p-1022"),  # least normal
    0.25,
    math.nextafter(1.0, 0.0),
    1.0,
    math.nextafter(1.0, math.inf),
    1.33,
    math.nextafter(2.0, 0.0),
    2.0,
    math.nextafter(2.0, math.inf),
    3.5,
    123.456,
    math.nextafter(2.0**52, 0.0),
    2.0**52,
    math.nextafter(2.0**53, 0.0),
    2.0**53,
    float.fromhex("0x1.fffffffffffffp+1023"),  # greatest finite float
]

rng = random.Random(0x2A11D17)
generated: list[float] = []
while len(generated) < 50_000:
    raw = rng.getrandbits(64) & 0x7FFF_FFFF_FFFF_FFFF
    value = struct.unpack(">d", raw.to_bytes(8, "big"))[0]
    if value > 0.0 and math.isfinite(value):
        generated.append(value)

mismatches: list[tuple[float, object, object]] = []
for value in explicit + generated:
    expected = canonical.truncate_number(value)
    actual = candidate.truncate_number(value)
    if bits(expected) != bits(actual):
        mismatches.append((value, expected, actual))

print(f"documented_and_boundary_cases={len(explicit)}")
for value in explicit:
    expected = canonical.truncate_number(value)
    actual = candidate.truncate_number(value)
    print(
        f"case={value.hex()} input_bits={bits(value)} "
        f"canonical={expected.hex()} candidate={actual.hex()}"
    )
print(f"generated_seed=0x2A11D17 generated_positive_finite={len(generated)}")
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:20]:
        print(f"MISMATCH {mismatch!r}")
    raise SystemExit(1)

# Explicitly record adjacent excluded boundaries rather than folding them into
# the intended positive-finite domain.
print(
    "outside_domain_zero="
    f"{canonical.truncate_number(0.0)!r}/{candidate.truncate_number(0.0)!r}"
)
print(
    "outside_domain_negative="
    f"{canonical.truncate_number(-3.5)!r}/{candidate.truncate_number(-3.5)!r}"
)
try:
    candidate_inf: object = candidate.truncate_number(math.inf)
except Exception as error:  # evidence only: infinity is not decomposable as stated
    candidate_inf = f"{type(error).__name__}: {error}"
print(
    "outside_domain_positive_infinity="
    f"{canonical.truncate_number(math.inf)!r}/{candidate_inf!r}"
)
print("STAGE2_DIFFERENTIAL_OK")
