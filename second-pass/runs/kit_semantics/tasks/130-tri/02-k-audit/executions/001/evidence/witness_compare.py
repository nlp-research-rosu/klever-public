#!/usr/bin/env python3
"""Compare concrete instances of the K postcondition with both Python entries."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
EXPECTED = {
    0: [1],
    3: [1, 3, 2, 8],
    4: [1, 3, 2, 8, 3],
    10: [1, 3, 2, 8, 3, 15, 4, 24, 5, 35, 6],
}


def load_tri(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.tri


def main() -> int:
    canonical = load_tri("witness_canonical", ROOT / "canonical.py")
    generated = load_tri("witness_generated", ROOT / "solution.py")
    ok = True
    for n, k_postcondition in EXPECTED.items():
        canonical_result = canonical(n)
        generated_result = generated(n)
        equal = canonical_result == generated_result == k_postcondition
        ok &= equal
        print(f"N={n} satisfies_entry_precondition={n >= 0}")
        print(f"  K_triResult={k_postcondition!r}")
        print(f"  trusted_canonical={canonical_result!r}")
        print(f"  generated_solution={generated_result!r}")
        print(f"  numeric_list_equality={equal}")
    print(
        "loop_witness=N=3,I=0,L=1,H=0,P=.ValSeq; "
        "guards N>=0, I>=0, I<=N+1 are all true"
    )
    print("OVERALL=" + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
