#!/usr/bin/env python3
"""Ground witnesses for the two entry-claim preconditions and results."""

from __future__ import annotations

import importlib.util
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/63-fibfib")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("witness_canonical", SCRATCH / "trusted/canonical.py")
submitted = load_module(
    "witness_submitted", SCRATCH / "candidate-src/solution.py"
)


def contract_fibfib(n: int) -> int:
    a, b, c = 0, 0, 1
    for _ in range(n):
        a, b, c = b, c, a + b + c
    return a


for n in [0, 2, 5, 8]:
    contract = contract_fibfib(n)
    trusted = canonical.fibfib(n)
    candidate = submitted.fibfib(n)
    print(
        f"program_ground N={n} precondition=(0 <= {n})={0 <= n}"
        f" claimed_result=fibfibMath({n})={contract}"
        f" canonical={trusted} submitted={candidate}"
        f" all_equal={contract == trusted == candidate}"
    )

n = 5
i = 2
initial_env = {
    "a": contract_fibfib(i),
    "b": contract_fibfib(i + 1),
    "c": contract_fibfib(i + 2),
    "i": i,
    "n": n,
}
final_env = {
    "a": contract_fibfib(n),
    "b": contract_fibfib(n + 1),
    "c": contract_fibfib(n + 2),
    "i": n,
    "n": n,
}
print(
    f"loop_ground I={i} N={n}"
    f" precondition=(0 <= {i} <= {n})={0 <= i <= n}"
    f" initial_env={initial_env} initial_result=77"
)
print(
    f"loop_claimed_final_env={final_env}"
    f" claimed_result={contract_fibfib(n)}"
    f" canonical={canonical.fibfib(n)} submitted={submitted.fibfib(n)}"
)
