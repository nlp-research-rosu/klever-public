#!/usr/bin/env python3
import importlib.util


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check_dict_case


canonical = load("canonical_witness", "/tmp/audit-work/trusted/canonical.py")
generated = load("generated_witness", "/tmp/audit-work/work/solution.py")


def contract(value):
    return bool(value) and (
        all(isinstance(key, str) and key.islower() for key in value)
        or all(isinstance(key, str) and key.isupper() for key in value)
    )


cases = [
    ("empty", {}),
    ("ascii-lower", {"a": 0}),
    ("ascii-upper", {"A": 0}),
    ("ascii-mixed", {"a": 0, "A": 1}),
    ("non-string", {8: 0}),
    ("unicode-lower", {"é": 0}),
    ("canonical-early-break", {"a": 0, "b2": 1, "A": 2}),
]
for name, value in cases:
    print(
        f"{name}: input={value!r} canonical={canonical(value)!r} "
        f"generated={generated(value)!r} prompt_contract={contract(value)!r}"
    )
