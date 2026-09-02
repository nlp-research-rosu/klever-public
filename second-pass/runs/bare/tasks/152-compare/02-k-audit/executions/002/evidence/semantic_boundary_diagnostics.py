#!/usr/bin/env python3
"""Witnesses for generated-semantics behavior outside the clear integer-pair subset."""

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


def outcome(function, game, guess):
    try:
        return f"returned:{function(game, guess)!r}"
    except Exception as err:
        return f"raised:{type(err).__name__}:{err}"


canonical = load("trusted_canonical_boundary", "/reference/canonical.py").compare
submitted = load("submitted_boundary", f"{SCRATCH}/solution.py").compare

cases = [
    (
        "short_guess",
        [7],
        [],
        "VList(VCons(VInt(7),VNil))",
        "VList(VNil)",
    ),
    (
        "long_guess",
        [],
        [7],
        "VList(VNil)",
        "VList(VCons(VInt(7),VNil))",
    ),
    (
        "bool_scores",
        [True],
        [False],
        "VList(VCons(VBool(true),VNil))",
        "VList(VCons(VBool(false),VNil))",
    ),
]

for label, game, guess, game_term, guess_term in cases:
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        "reviewer-semantic-kompiled",
        f"-cGAME={game_term}",
        f"-cGUESS={guess_term}",
    ]
    run = subprocess.run(
        command,
        cwd=SCRATCH,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(f"case={label} command={' '.join(command)}")
    print(
        f"case={label} canonical={outcome(canonical, game, guess)} "
        f"submitted={outcome(submitted, game, guess)}"
    )
    print(f"case={label} krun_exit={run.returncode} krun_output={run.stdout.strip()!r}")
