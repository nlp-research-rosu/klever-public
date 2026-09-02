#!/usr/bin/env python3

"""Ground substitutions for the symbolic entry claim."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path("/tmp/audit-work/49-modp")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.modp


canonical = load("stage4_canonical", ROOT / "trusted-canonical.py")
generated = load("stage4_generated", ROOT / "solution.py")
witnesses = [(3, 5), (1101, 101), (0, 101), (0, 1), (1, -5), (0, -5)]

print(
    'state=<env>0</env>; scope 0 binds "modp" to exact translated closure; '
    "scopeLoc=1; empty heap/stack; noRet; NoExc; exit-code=0"
)
for n, p in witnesses:
    precondition = n >= 0 and p != 0
    claimed = (2**n) % p
    print(
        f"N={n} P={p} precondition={precondition} claimed={claimed!r} "
        f"generated={generated(n, p)!r} canonical={canonical(n, p)!r}"
    )

raise SystemExit(0)
