#!/usr/bin/env python3
"""Concrete generated-semantics comparison against both Python implementations."""

from __future__ import annotations

import importlib.util
import subprocess


SCRATCH = "/tmp/audit-work/152-compare"


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def values(items: list[int]) -> str:
    term = "VNil"
    for item in reversed(items):
        term = f"VCons(VInt({item}),{term})"
    return term


def value(items: list[int]) -> str:
    return f"VList({values(items)})"


def normalize(text: str) -> str:
    return "".join(text.split())


canonical = load("trusted_canonical_kdiff", "/reference/canonical.py").compare
submitted = load("submitted_kdiff", f"{SCRATCH}/solution.py").compare

cases = [
    ([], []),
    ([0], [1]),       # negative difference branch
    ([0], [0]),       # equality boundary
    ([1], [0]),       # positive difference branch
    ([-1], [0]),
    ([0], [-1]),
    ([-3, 2, 0], [4, -2, 0]),
    ([1, 2, 3, 4, 5, 1], [1, 2, 3, 4, 2, -2]),
    ([0, 5, 0, 0, 0, 4], [4, 1, 1, 0, 0, -2]),
    ([-10**40, 10**40], [10**40, -(10**40)]),
]

mismatches = 0
for number, (game, guess) in enumerate(cases):
    canonical_result = canonical(game, guess)
    submitted_result = submitted(game, guess)
    game_term = value(game)
    guess_term = value(guess)
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        "reviewer-semantic-kompiled",
        f"-cGAME={game_term}",
        f"-cGUESS={guess_term}",
    ]
    print(f"case={number} command={' '.join(command)}")
    run = subprocess.run(
        command,
        cwd=SCRATCH,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    expected_k = normalize(f"<k>{value(canonical_result)}~>.K</k>")
    actual_k = normalize(run.stdout)
    equal = (
        run.returncode == 0
        and submitted_result == canonical_result
        and actual_k == expected_k
    )
    print(
        f"case={number} exit={run.returncode} game={game!r} guess={guess!r} "
        f"canonical={canonical_result!r} submitted={submitted_result!r}"
    )
    print(f"case={number} krun_output={run.stdout.strip()!r}")
    print(f"case={number} expected_normalized={expected_k} equal={equal}")
    if not equal:
        mismatches += 1

print(f"case_count={len(cases)} mismatch_count={mismatches}")
if mismatches:
    raise SystemExit(1)
