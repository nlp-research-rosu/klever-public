#!/usr/bin/env python3
"""Ground counterexample for the fresh +1 result mutation."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path("/tmp/audit-work/36-fizz-buzz-audit-002")


def load(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fizz_buzz


candidate = load("candidate_mutation_witness", ROOT / "candidate" / "solution.py")
canonical = load("canonical_mutation_witness", ROOT / "trusted" / "canonical.py")
n = 0
actual_candidate = candidate(n)
actual_canonical = canonical(n)
mutated_required = actual_candidate + 1
print("entry_precondition=true (the original entry claim has no requires clause)")
print(
    f"N={n} candidate_result={actual_candidate} canonical_result={actual_canonical} "
    f"mutated_required_result={mutated_required}"
)
assert actual_candidate == actual_canonical == 0
assert mutated_required == 1
