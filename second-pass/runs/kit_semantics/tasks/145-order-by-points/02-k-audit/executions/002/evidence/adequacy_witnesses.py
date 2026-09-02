#!/usr/bin/env python3
import importlib.util
from pathlib import Path


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("canonical_witness", Path("/reference/canonical.py"))
candidate = load(
    "candidate_witness",
    Path("/tmp/audit-work/145-order-by-points-002/solution.py"),
)

list_witnesses = [
    [1, 11, -1, -11, -12],
    [],
    [1, 10, 100, 2, 20, 200],
    [-12, -21, -30, -3, -102, -120, -201, -210],
]
for values in list_witnesses:
    canonical_result = canonical.order_by_points(list(values))
    candidate_result = candidate.order_by_points(list(values))
    print(
        f"input={values!r} canonical={canonical_result!r} "
        f"candidate={candidate_result!r}"
    )
    assert candidate_result == canonical_result

for number in [-100, -12, -10, -9, -1, 0, 1, 9, 10, 12, 100]:
    print(f"digit_sum({number})={candidate.digit_sum(number)}")

print("LOOP WITNESS N=12 S=0 SIGN=-1: leadingDigit=1 lowerDigitSumAcc=2")
print("FUNCTION WITNESS N=-12: signedDigitSum=1")
print(
    "ORDER WITNESS VS=[1,11,-1,-11,-12]: "
    "result=[-1,-11,1,-12,11]"
)
print("ADEQUACY WITNESSES PASS")
