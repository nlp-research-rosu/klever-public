#!/usr/bin/env python3
"""Ground instances of the formal postcondition versus both Python programs."""

from __future__ import annotations

import importlib.util
from pathlib import Path


WORK = Path("/tmp/audit-work/49-modp")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    canonical = load("witness_canonical", WORK / "canonical.py")
    candidate = load("witness_candidate", WORK / "solution.py")
    witnesses = [(0, 1), (0, 101), (1, 1), (3, 5), (1101, 101)]
    print("FORMAL_PRECONDITION n >= 0 and p > 0")
    for n, p in witnesses:
        # Under p > 0, K's pyMod(2 ^Int n, p) is Python's pow(2,n,p).
        formal = pow(2, n, p)
        print(
            f"WITNESS n={n} p={p} satisfies=True "
            f"formal={formal} generated={candidate.modp(n, p)!r} "
            f"canonical={canonical.modp(n, p)!r}"
        )


if __name__ == "__main__":
    main()
