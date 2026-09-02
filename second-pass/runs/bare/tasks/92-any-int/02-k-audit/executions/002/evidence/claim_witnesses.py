#!/usr/bin/env python3
"""Show one satisfying ground witness for each of the seven entry claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.any_int


def main() -> None:
    canonical = load(Path("/reference/canonical.py"), "canonical_witness")
    generated = load(
        Path("/tmp/audit-work/92-any-int/candidate/solution.py"),
        "generated_witness",
    )
    witnesses = [
        ("claim-1", (5, 2, 7), "x+y=z", True),
        ("claim-2", (2, 5, 3), "x+y!=z and x+z=y", True),
        ("claim-3", (5, 2, 3), "x+y!=z and x+z!=y and y+z=x", True),
        ("claim-4", (3, 2, 2), "all three equalities false", False),
        ("claim-5", (1.0, 2, 3), "first argument non-int", False),
        ("claim-6", (1, 2.0, 3), "second argument first non-int", False),
        ("claim-7", (1, 2, 3.0), "third argument first non-int", False),
    ]
    for label, args, precondition, claimed in witnesses:
        canonical_result = canonical(*args)
        generated_result = generated(*args)
        ok = canonical_result is claimed and generated_result is claimed
        print(
            f"{label}: args={args!r}; precondition={precondition}; "
            f"claimed={claimed}; canonical={canonical_result}; "
            f"generated={generated_result}; match={ok}"
        )
        if not ok:
            raise SystemExit(1)
    print("TOTAL_WITNESSES: 7")
    print("TOTAL_FAILURES: 0")


if __name__ == "__main__":
    main()
