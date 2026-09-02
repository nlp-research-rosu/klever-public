#!/usr/bin/env python3
"""Ground witnesses for the sole MODP-SPEC entry claim."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any, Callable


def load(path: Path, name: str) -> Callable[[int, int], Any]:
    module_spec = importlib.util.spec_from_file_location(name, path)
    if module_spec is None or module_spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module.modp


canonical = load(
    Path("/tmp/audit-work/49-modp/trusted/canonical.py"), "witness_canonical"
)
solution = load(Path("/tmp/audit-work/49-modp/solution.py"), "witness_solution")

witnesses = [(3, 5), (0, 1)]
for n, p in witnesses:
    assert n >= 0 and p > 0
    record = {
        "input": {"N": n, "P": p},
        "precondition": n >= 0 and p > 0,
        "claimed_specModp": pow(2, n) % p,
        "submitted_solution": solution(n, p),
        "trusted_canonical": canonical(n, p),
    }
    print(json.dumps(record, sort_keys=True))
