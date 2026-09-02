#!/usr/bin/env python3
"""Show a concrete satisfying input and both Python results."""

from __future__ import annotations

import importlib.util
import pathlib


SCRATCH = pathlib.Path("/tmp/audit-work/33-sort-third")


def load(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_third


source = [5, 6, 3, 4, 8, 9, 2]
formal_substitution = [2, 6, 3, 4, 8, 9, 5]
canonical_result = load("canonical_ground", SCRATCH / "canonical.py")(source)
candidate_result = load("candidate_ground", SCRATCH / "solution.py")(source)
print(f"input={source}")
print(f"formal_substitution={formal_substitution}")
print(f"trusted_canonical={canonical_result}")
print(f"generated_solution={candidate_result}")
print(
    "all_equal="
    + str(formal_substitution == canonical_result == candidate_result)
)
raise SystemExit(
    0 if formal_substitution == canonical_result == candidate_result else 1
)
