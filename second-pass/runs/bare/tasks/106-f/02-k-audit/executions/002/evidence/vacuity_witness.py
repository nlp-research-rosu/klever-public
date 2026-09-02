#!/usr/bin/env python3
"""Ground falsity witness for the fresh extra-zero postcondition mutation."""

import importlib.util
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.f


n = 0
canonical = load_entry(Path("/reference/canonical.py"), "vac_canonical")
candidate = load_entry(
    Path("/tmp/audit-work/reconstruction/solution.py"), "vac_candidate"
)
actual_canonical = canonical(n)
actual_candidate = candidate(n)
mutated_obligation = actual_canonical + [0]
print(f"satisfying input n={n}, precondition n>=0 is {n >= 0}")
print(f"canonical_result={actual_canonical}")
print(f"candidate_result={actual_candidate}")
print(f"mutated_required_result={mutated_obligation}")
print(
    "false_for_witness="
    f"{actual_canonical == actual_candidate and actual_candidate != mutated_obligation}"
)
