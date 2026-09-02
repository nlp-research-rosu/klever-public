#!/usr/bin/env python3
"""Concrete witness for both entry preconditions and result substitution."""

import importlib.util
import pathlib


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, pathlib.Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.vowels_count


canonical = load(
    "/tmp/audit-work/proof/trusted/canonical.py", "witness_canonical"
)
generated = load("/tmp/audit-work/proof/solution.py", "witness_generated")

text = "ACEDY"
claimed_result = 3
scope_context = {}
print(f"main_S_codepoints={[ord(char) for char in text]}")
print(f"main_claimed_result={claimed_result}")
print(f"canonical_result={canonical(text)}")
print(f"generated_result={generated(text)}")
print("loop_SC={}")
print(f"loop_guard_1_not_in_SC={1 not in scope_context}")
print("loop_initial_count=2")
print("loop_iterable='acedy'")
print("loop_expected_count=4")
print("loop_expected_char='y'")
print("loop_expected_last_y=true")

assert canonical(text) == claimed_result
assert generated(text) == claimed_result
assert 1 not in scope_context
