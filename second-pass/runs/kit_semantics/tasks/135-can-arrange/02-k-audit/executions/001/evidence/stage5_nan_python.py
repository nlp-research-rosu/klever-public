"""Concrete CPython side of the supplied-model NaN divergence witness."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scratch = Path("/tmp/audit-work/135-can-arrange")
candidate = load("nan_solution", scratch / "solution.py")
canonical = load("nan_canonical", scratch / "trusted-canonical.py")
witness = [float("nan"), 1.0]

print("witness", repr(witness))
print("python_nan_ge_one", witness[0] >= witness[1])
print("python_one_ge_nan", witness[1] >= witness[0])
print("candidate_literal_not_ge_result", candidate.can_arrange(witness))
print("canonical_less_than_result", canonical.can_arrange(witness))

assert candidate.can_arrange(witness) == 1
