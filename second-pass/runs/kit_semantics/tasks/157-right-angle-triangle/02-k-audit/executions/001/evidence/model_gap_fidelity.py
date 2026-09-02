#!/usr/bin/env python3
"""Check canonical/candidate behavior on the supplied-model divergence witness."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any, Callable


def load_entry(path: Path) -> Callable[[Any, Any, Any], Any]:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.right_angle_triangle


def outcome(fn: Callable[[Any, Any, Any], Any], args: tuple[Any, Any, Any]) -> tuple[str, str]:
    try:
        return ("return", repr(fn(*args)))
    except BaseException as error:
        return ("raise", type(error).__name__)


witness = (10**308, 1.0e308, 1.0e308)
canonical = load_entry(Path("/reference/canonical.py"))
candidate = load_entry(Path("/candidate/solution.py"))
canonical_outcome = outcome(canonical, witness)
candidate_outcome = outcome(candidate, witness)

print(f"WITNESS={witness!r}")
print(f"CANONICAL={canonical_outcome!r}")
print(f"CANDIDATE={candidate_outcome!r}")
print(f"MATCH={canonical_outcome == candidate_outcome}")

assert canonical_outcome == ("raise", "OverflowError")
assert candidate_outcome == canonical_outcome
