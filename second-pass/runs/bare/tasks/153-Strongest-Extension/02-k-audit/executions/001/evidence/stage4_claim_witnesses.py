#!/usr/bin/env python3
"""Concrete satisfiability and result checks for all seven entry claims."""

from __future__ import annotations

import importlib.util
import json


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Strongest_Extension


canonical = load("/reference/canonical.py", "canonical_claim_witness")
candidate = load("/tmp/audit-work/candidate-src/solution.py", "candidate_claim_witness")

# Each row instantiates the exact initial cells in one submitted claim:
# env=.Map, functions=.Map, result=noResult, and the listed class/extensions.
cases = [
    ("claim-1-worked", "Slices", ["SErviNGSliCes", "Cheese", "StuFfed"], "Slices.SErviNGSliCes"),
    ("claim-2-tie", "Witness", ["AA", "Be", "CC"], "Witness.AA"),
    ("claim-3-strict-replace", "Witness", ["abc", "AB", "A-b"], "Witness.AB"),
    ("claim-4-uncased", "Witness", ["a-1", "--", "A!"], "Witness.A!"),
    ("claim-5-empty-name", "Witness", ["", "123", "!"], "Witness."),
    ("claim-6-negative", "Witness", ["abcd", "a", "xy"], "Witness.a"),
    ("claim-7-singleton", "Witness", ["Zz"], "Witness.Zz"),
]

failures = []
for label, class_name, extensions, claimed in cases:
    row = {
        "claim": label,
        "satisfying_initial_state": {
            "k": "StrongestProgram ~> #start",
            "env": ".Map",
            "functions": ".Map",
            "inputClass": class_name,
            "inputExtensions": extensions,
            "result": "noResult",
        },
        "claimed_result_after_refStrongest_reduction": claimed,
        "canonical_result": canonical(class_name, extensions),
        "candidate_python_result": candidate(class_name, extensions),
    }
    row["all_equal"] = (
        row["claimed_result_after_refStrongest_reduction"]
        == row["canonical_result"]
        == row["candidate_python_result"]
    )
    if not row["all_equal"]:
        failures.append(row)
    print(json.dumps(row, ensure_ascii=False))

print(json.dumps({"witnesses": len(cases), "failures": len(failures)}))
raise SystemExit(1 if failures else 0)
