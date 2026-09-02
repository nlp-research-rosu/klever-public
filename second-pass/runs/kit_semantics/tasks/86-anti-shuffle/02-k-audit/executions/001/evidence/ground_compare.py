#!/usr/bin/env python3
"""Print the Python-side values used by auditor-ground-spec.k."""

import importlib.util
from pathlib import Path


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.anti_shuffle


root = Path("/tmp/audit-work/anti-shuffle")
canonical = load("canonical_ground", root / "canonical.py")
candidate = load("candidate_ground", root / "solution.py")
for value in ("", "ba a", "aa"):
    print(
        f"input={value!r} canonical={canonical(value)!r} "
        f"candidate={candidate(value)!r}"
    )
