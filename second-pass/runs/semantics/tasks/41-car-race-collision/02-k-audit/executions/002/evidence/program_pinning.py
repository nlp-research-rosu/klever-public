#!/usr/bin/env python3
"""Mechanical constructor comparison plus concrete claim-result witnesses."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/reconstruct")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def balanced_constructor(text: str, start: int) -> str:
    opening = text.index("Module(", start)
    depth = 0
    in_string = False
    escaped = False
    for index in range(opening, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[opening : index + 1]
    raise ValueError("unterminated Module constructor")


def tokens(term: str) -> list[str]:
    return re.findall(r'"(?:\\.|[^"\\])*"|[A-Za-z_][A-Za-z0-9_-]*|[(),]', term)


solution_text = (SCRATCH / "solution.regenerated.mpy").read_text(encoding="utf-8")
verification_text = (SCRATCH / "verification.k").read_text(encoding="utf-8")
embedded_text = balanced_constructor(
    verification_text, verification_text.index("rule solutionModule")
)

solution_tokens = tokens(solution_text)
embedded_tokens = tokens(embedded_text)
module_match = solution_tokens == embedded_tokens

run_rule_match = bool(
    re.search(
        r"rule\s+#runCarRaceCollision\(N:Int\)\s*"
        r"=>\s*#loadAll\(solutionModule\)\s*~>\s*"
        r'Call\(Name\("car_race_collision"\),\s*Int\(N\)\)',
        verification_text,
        re.DOTALL,
    )
)

canonical = load_module("trusted_canonical", Path("/reference/canonical.py"))
candidate = load_module("scratch_candidate", SCRATCH / "solution.py")
witnesses = []
for value in [0, 3, 10, -2]:
    claim_result = value * value
    canonical_result = canonical.car_race_collision(value)
    candidate_result = candidate.car_race_collision(value)
    witnesses.append(
        {
            "N": value,
            "formal_initial_cells": {
                "k": f"#runCarRaceCollision({value})",
                "env": 0,
                "scope_0": "scope(.Map, parent(-1))",
                "scope_-1": "builtinsScope",
                "scopeLoc": 1,
                "heap": ".Map",
                "heapLoc": 0,
                "stack": ".List",
                "ret": "noRet",
                "exc": "NoExc",
                "exit-code": 0,
            },
            "claimed_result": claim_result,
            "canonical_result": canonical_result,
            "candidate_result": candidate_result,
            "all_equal": claim_result == canonical_result == candidate_result,
        }
    )

report = {
    "trusted_regenerated_module_term": solution_text.strip(),
    "verification_embedded_module_term": embedded_text.strip(),
    "constructor_token_match": module_match,
    "constructor_tokens": solution_tokens,
    "run_wrapper_exact_load_then_call_match": run_rule_match,
    "claim_has_no_requires_clause": "requires" not in (
        SCRATCH / "spec.k"
    ).read_text(encoding="utf-8").split("claim", 1)[1],
    "witnesses": witnesses,
}
print(json.dumps(report, indent=2, sort_keys=True))

ok = module_match and run_rule_match and all(item["all_equal"] for item in witnesses)
sys.exit(0 if ok else 1)
