#!/usr/bin/env python3
"""Ground witnesses for every entry claim and the intended arithmetic result."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Callable


def load(path: str, module_name: str) -> Callable[[str, int], int]:
    spec = importlib.util.spec_from_file_location(module_name, Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fruit_distribution


candidate = load("/tmp/audit-work/fresh/solution.py", "adequacy_candidate")
canonical = load("/reference/canonical.py", "adequacy_canonical")

# The first witness instantiates A=5, O=6, N=19 in the general claim.
# The remaining rows instantiate all four concrete entry claims.
witnesses = [
    {
        "claim": "general (A=5,O=6,N=19)",
        "A": 5,
        "O": 6,
        "N": 19,
        "s": "5 apples and 6 oranges",
        "claimed": 8,
        "precondition": (5 >= 0 and 6 >= 0 and 19 >= 5 + 6),
    },
    {
        "claim": "example-1",
        "A": 5,
        "O": 6,
        "N": 19,
        "s": "5 apples and 6 oranges",
        "claimed": 8,
        "precondition": True,
    },
    {
        "claim": "example-2",
        "A": 0,
        "O": 1,
        "N": 3,
        "s": "0 apples and 1 oranges",
        "claimed": 2,
        "precondition": True,
    },
    {
        "claim": "example-3",
        "A": 2,
        "O": 3,
        "N": 100,
        "s": "2 apples and 3 oranges",
        "claimed": 95,
        "precondition": True,
    },
    {
        "claim": "example-4",
        "A": 100,
        "O": 1,
        "N": 120,
        "s": "100 apples and 1 oranges",
        "claimed": 19,
        "precondition": True,
    },
]

failures = 0
for witness in witnesses:
    record = dict(witness)
    record["arithmetic"] = witness["N"] - witness["A"] - witness["O"]
    record["candidate_python"] = candidate(witness["s"], witness["N"])
    record["canonical_python"] = canonical(witness["s"], witness["N"])
    record["agrees"] = (
        witness["precondition"]
        and record["arithmetic"]
        == record["candidate_python"]
        == record["canonical_python"]
        == witness["claimed"]
    )
    failures += int(not record["agrees"])
    print(json.dumps(record, sort_keys=True))

print(f"witness_failure_count={failures}")
raise SystemExit(1 if failures else 0)
