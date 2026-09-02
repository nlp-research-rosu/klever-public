#!/usr/bin/env python3
"""A concrete satisfiable instance of the universal entry claim."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.compare


canonical = load_entry(
    "trusted_canonical_ground",
    Path("/tmp/audit-work/152-compare/trusted/canonical.py"),
)
generated = load_entry(
    "candidate_generated_ground",
    Path("/tmp/audit-work/152-compare/candidate/solution.py"),
)

game = [1, -2, 3]
guess = [4, -2, -5]
claimed = [3, 0, 8]
canonical_result = canonical(game.copy(), guess.copy())
generated_result = generated(game.copy(), guess.copy())

print(f"GAME={game}")
print(f"GUESS={guess}")
print(f"claim_absDiffs_value={claimed}")
print(f"trusted_canonical_result={canonical_result}")
print(f"generated_result={generated_result}")
print(
    "all_equal="
    f"{claimed == canonical_result == generated_result}"
)
assert claimed == canonical_result == generated_result
