#!/usr/bin/env python3
"""Ground satisfying inputs and both Python results."""

import importlib.util
from pathlib import Path


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.intersperse


canonical = load("witness_canonical", "/reference/canonical.py")
generated = load("witness_generated", "/tmp/audit-work/candidate/solution.py")

for numbers, delimiter in [([], 4), ([1, 2, 3], 4)]:
    claimed = [] if not numbers else [1, 4, 2, 4, 3]
    canonical_result = canonical(list(numbers), delimiter)
    generated_result = generated(list(numbers), delimiter)
    print(f"input={numbers!r}, delimiter={delimiter!r}")
    print(f"claimed={claimed!r}")
    print(f"canonical={canonical_result!r}")
    print(f"generated={generated_result!r}")
    assert claimed == canonical_result == generated_result
