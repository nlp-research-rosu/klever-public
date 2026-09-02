#!/usr/bin/env python3
"""Compare the concrete K substitution targets with both Python functions."""

from __future__ import annotations

import importlib.util
from pathlib import Path


WORK = Path("/tmp/audit-work/25-factorize")
K_TARGETS = {
    1: [],
    8: [2, 2, 2],
    70: [2, 5, 7],
}


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.factorize


def main() -> int:
    canonical = load("canonical_substitution", WORK / "canonical.py")
    candidate = load("candidate_substitution", WORK / "solution.py")
    ok = True
    for n, k_target in K_TARGETS.items():
        canonical_value = canonical(n)
        candidate_value = candidate(n)
        match = k_target == canonical_value == candidate_value
        ok &= match
        print(
            f"N={n} K_target={k_target} canonical={canonical_value} "
            f"candidate={candidate_value} all_equal={match}"
        )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
