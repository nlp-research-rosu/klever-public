#!/usr/bin/env python3
import importlib.util
from pathlib import Path


scratch = Path("/tmp/audit-work/0-has-close-elements")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("trusted_canonical_witness", scratch / "canonical.py")
candidate = load("candidate_solution_witness", scratch / "solution.py")

numbers = [1.0, 1.0]
threshold = 0.1
contract_result = any(
    abs(numbers[i] - numbers[j]) < threshold
    for i in range(len(numbers))
    for j in range(i + 1, len(numbers))
)

print(f"numbers={numbers!r}")
print(f"threshold={threshold!r}")
print(f"hasPairs_ground_reduction={contract_result!r}")
print(f"canonical={canonical.has_close_elements(numbers, threshold)!r}")
print(f"candidate={candidate.has_close_elements(numbers, threshold)!r}")
assert contract_result is True
assert canonical.has_close_elements(numbers, threshold) == contract_result
assert candidate.has_close_elements(numbers, threshold) == contract_result
