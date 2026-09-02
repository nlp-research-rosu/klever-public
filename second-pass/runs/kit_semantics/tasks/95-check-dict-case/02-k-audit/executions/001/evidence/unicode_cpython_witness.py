#!/usr/bin/env python3
"""Concrete CPython side of the supplied-model Unicode divergence witness."""

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check_dict_case


candidate = load(Path("/tmp/audit-work/95-check-dict-case/solution.py"), "candidate_unicode")
canonical = load(Path("/reference/canonical.py"), "canonical_unicode")
witness = {"é": 1}
print('"é".islower() =', "é".islower())
print("candidate({'é': 1}) =", candidate(witness))
print("canonical({'é': 1}) =", canonical(witness))
