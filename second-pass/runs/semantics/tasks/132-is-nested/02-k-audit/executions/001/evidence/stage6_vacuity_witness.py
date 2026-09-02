#!/usr/bin/env python3
"""Show a satisfying concrete input that falsifies the audit mutation."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_nested


canonical = load("canonical_stage6", "/reference/canonical.py")
generated = load(
    "generated_stage6", "/tmp/audit-work/132-is-nested/source/solution.py"
)

value = ""
actual_canonical = canonical(value)
actual_generated = generated(value)
mutated_postcondition = not False  # not nested(bNil)
print(
    f"BS=bNil input={value!r}: canonical={actual_canonical} "
    f"generated={actual_generated} mutated_postcondition={mutated_postcondition}"
)
assert actual_canonical is False
assert actual_generated is False
assert mutated_postcondition is True
