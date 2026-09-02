#!/usr/bin/env python3
import importlib.util


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check_dict_case


canonical = load("/tmp/audit-work/trusted/canonical.py", "canonical")
generated = load("/tmp/audit-work/src/solution.py", "generated")

cases = [
    {},
    {"a": 0},
    {"A": 0},
    {"123": 0},
    {7: 0},
    {"a": 0, "b": 0, "A": 0},
    {"é": 0},
]

for value in cases:
    print(
        repr(value),
        "canonical=", canonical(value),
        "generated=", generated(value),
    )
