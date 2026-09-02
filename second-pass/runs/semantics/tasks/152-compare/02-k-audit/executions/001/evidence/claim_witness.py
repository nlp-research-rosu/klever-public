#!/usr/bin/env python3
"""Concrete satisfying substitutions for every entry-claim shape."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("trusted_canonical_witness", "/reference/canonical.py")
generated = load(
    "generated_solution_witness",
    "/tmp/audit-work/compare152/source/solution.py",
)

witnesses = [
    {
        "claim": "universal claim",
        "GAME_IntSeq": [1, -2],
        "GUESS_IntSeq": [4, -2],
        "K_absDiffs_substitution": [3, 0],
    },
    {
        "claim": "prompt example claim 1",
        "GAME_IntSeq": [1, 2, 3, 4, 5, 1],
        "GUESS_IntSeq": [1, 2, 3, 4, 2, -2],
        "K_absDiffs_substitution": [0, 0, 0, 0, 3, 3],
    },
    {
        "claim": "prompt example claim 2",
        "GAME_IntSeq": [0, 5, 0, 0, 0, 4],
        "GUESS_IntSeq": [4, 1, 1, 0, 0, -2],
        "K_absDiffs_substitution": [4, 4, 1, 0, 0, 6],
    },
]

for witness in witnesses:
    game = witness["GAME_IntSeq"]
    guess = witness["GUESS_IntSeq"]
    witness["canonical_result"] = canonical.compare(game, guess)
    witness["generated_result"] = generated.compare(game, guess)
    witness["results_all_equal"] = (
        witness["canonical_result"]
        == witness["generated_result"]
        == witness["K_absDiffs_substitution"]
    )

payload = {
    "common_precondition_cells": {
        "k_prefix": "compareDef ~> Call(Name(\"compare\"), list(intVals(GAME)), list(intVals(GUESS)))",
        "env": 0,
        "module_scope": "0 |-> scope(.Map, parent(-1))",
        "builtins_scope": "-1 |-> builtinsScope",
        "scopeLoc": 1,
        "heap": ".Map",
        "heapLoc": 0,
        "stack": ".List",
        "ret": "noRet",
        "exc": "NoExc",
    },
    "witnesses": witnesses,
}
print(json.dumps(payload, indent=2, sort_keys=True))
raise SystemExit(0 if all(w["results_all_equal"] for w in witnesses) else 1)
