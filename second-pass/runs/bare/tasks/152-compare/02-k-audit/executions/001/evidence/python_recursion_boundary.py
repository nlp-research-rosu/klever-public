#!/usr/bin/env python3
"""Probe the CPython recursion-resource boundary on valid equal-length inputs."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/152-compare")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.compare


canonical = load(SCRATCH / "trusted" / "canonical.py", "canonical_recursion_probe")
generated = load(SCRATCH / "solution.py", "generated_recursion_probe")

print("PYTHON_VERSION:", sys.version.replace("\n", " "))
print("RECURSION_LIMIT:", sys.getrecursionlimit())
for length in [0, 1, 900, 1000, 1100]:
    game = [1] * length
    guess = [0] * length
    canonical_result = canonical(game, guess)
    try:
        generated_result = generated(game, guess)
    except Exception as error:
        generated_observation = f"{type(error).__name__}: {error}"
    else:
        generated_observation = (
            f"returned length={len(generated_result)} "
            f"correct={generated_result == canonical_result}"
        )
    print(
        f"LENGTH {length}: canonical_length={len(canonical_result)} "
        f"generated={generated_observation}"
    )
