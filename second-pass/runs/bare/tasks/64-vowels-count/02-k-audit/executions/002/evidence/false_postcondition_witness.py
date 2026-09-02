#!/usr/bin/env python3
"""Show that the fresh mutation is false on a satisfying intended input."""

from __future__ import annotations

import importlib.util
from pathlib import Path


WORK = Path("/tmp/audit-work/64-vowels-count")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.vowels_count


value = "abcde"
canonical = load(WORK / "trusted-canonical.py", "false_post_canonical")
generated = load(WORK / "solution.py", "false_post_generated")
canonical_result = canonical(value)
generated_result = generated(value)
mutated_postcondition = 3
print(f"satisfying_input={value!r}")
print("precondition_state=empty env, exact singleton vowels_count binding, empty stack")
print(f"trusted_canonical_result={canonical_result}")
print(f"generated_python_result={generated_result}")
print(f"mutated_required_result={mutated_postcondition}")
assert canonical_result == generated_result == 2
assert generated_result != mutated_postcondition
print("FALSE_MUTATION_WITNESS_CONFIRMED")
