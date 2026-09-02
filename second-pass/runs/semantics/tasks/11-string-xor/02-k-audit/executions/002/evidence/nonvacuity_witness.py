#!/usr/bin/env python3
"""Ground witness showing why the fresh postcondition mutation is false."""

import importlib.util
from pathlib import Path


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.string_xor


canonical = load(
    "canonical_nonvacuity",
    Path("/tmp/audit-work/11-string-xor/trusted/canonical.py"),
)
generated = load(
    "generated_nonvacuity",
    Path("/tmp/audit-work/11-string-xor/candidate/solution.py"),
)

a = ""
b = ""
canonical_result = canonical(a, b)
generated_result = generated(a, b)
mutated_required_result = canonical_result + "0"
print(f"input_a={a!r} input_b={b!r}")
print(f"canonical={canonical_result!r}")
print(f"generated={generated_result!r}")
print(f"mutated_required={mutated_required_result!r}")
assert canonical_result == generated_result == ""
assert generated_result != mutated_required_result
print("FALSE_MUTATION_WITNESS_OK")
