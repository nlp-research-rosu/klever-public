#!/usr/bin/env python3
"""A satisfiable ground witness for the submitted entry precondition."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def load(path: Path, name: str):
    spec = spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.rescale_to_unit


root = Path("/tmp/audit-work/21-rescale-to-unit-audit")
canonical = load(root / "canonical.py", "canonical_ground")
candidate = load(root / "solution.py", "candidate_ground")
values = [1.0, 2.0]

print("K input witness:")
print("  FIRST = 1.0")
print("  SECOND = 2.0")
print("  REST = .ValSeq")
print("  allFloats(.ValSeq) => true")
print(f"canonical.py result = {canonical(values.copy())!r}")
print(f"solution.py result  = {candidate(values.copy())!r}")
print("instantiated submitted postcondition:")
print(
    "  list(scaleAcc(.ValSeq, vCons(1.0, vCons(2.0, .ValSeq)), "
    "minVF(vCons(1.0, vCons(2.0, .ValSeq))), "
    "maxVF(vCons(1.0, vCons(2.0, .ValSeq)))))"
)
print(
    "The submitted theory provides no equation connecting either minVF/maxVF "
    "term to 1.0/2.0, so this postcondition cannot be reduced to [0.0, 1.0]."
)
