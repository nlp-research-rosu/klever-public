#!/usr/bin/env python3
"""Ground witnesses for all formal preconditions and the stated summary."""

from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_max_triples


def py_mod(left: int, right: int) -> int:
    return ((left % right) + right) % right


def choose_three(count: int) -> int:
    product = count * (count - 1) * (count - 2)
    return (product - py_mod(product, 6)) // 6


def zero_residues(n: int) -> int:
    return (n + 1 - py_mod(n + 1, 3)) // 3


def triple_count(n: int) -> int:
    zero = zero_residues(n)
    return choose_three(zero) + choose_three(n - zero)


def direct_contract(n: int) -> int:
    values = [i * i - i + 1 for i in range(1, n + 1)]
    return sum(
        (values[i] + values[j] + values[k]) % 3 == 0
        for i, j, k in itertools.combinations(range(n), 3)
    )


candidate = load("solution.py", "candidate_witness")
canonical = load("canonical.py", "canonical_witness")

print("residue preconditions: no requires clause; witnesses Q=-3..3")
for q in range(-3, 4):
    residues = (
        py_mod((3 * q) * (3 * q) - (3 * q) + 1, 3),
        py_mod((3 * q + 1) * (3 * q + 1) - (3 * q + 1) + 1, 3),
        py_mod((3 * q + 2) * (3 * q + 2) - (3 * q + 2) + 1, 3),
    )
    print(f"Q={q}: residues={residues}")
    assert residues == (1, 1, 0)

print("entry precondition: N > 0; concrete satisfying witnesses")
for n in (1, 2, 3, 4, 5, 8, 20, 64):
    formal = triple_count(n)
    row = (n, formal, candidate(n), canonical(n), direct_contract(n))
    print(f"N/formal/candidate/canonical/direct={row}")
    assert len(set(row[1:])) == 1
