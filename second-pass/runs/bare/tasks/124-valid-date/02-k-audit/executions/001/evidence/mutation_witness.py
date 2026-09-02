#!/usr/bin/env python3
"""Ground witness that makes the false mutation's precondition satisfiable."""

import importlib.util


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.valid_date


value = "03-11-2000"
canonical = load("/reference/canonical.py", "mutation_canonical")
generated = load("/tmp/audit-work/candidate-src/solution.py", "mutation_generated")
print(f"input={value!r}")
print(f"canonical={canonical(value)!r}")
print(f"generated={generated(value)!r}")
assert canonical(value) is True
assert generated(value) is True
