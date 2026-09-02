#!/usr/bin/env python3
"""Concrete satisfying witnesses for every entry/loop precondition."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.string_sequence


canonical = load(Path("/tmp/audit-work/trusted/canonical.py"), "canonical_witness")
candidate = load(
    Path("/tmp/audit-work/reconstruction/solution.py"), "candidate_witness"
)


def sequence_claim(n: int) -> str:
    return "" if n < 0 else " ".join(str(i) for i in range(n + 1))


entries = []
for claim, n in (("negative", -1), ("zero", 0), ("positive", 1)):
    entries.append(
        {
            "claim": claim,
            "n": n,
            "formal_precondition_satisfied": {
                "negative": n < 0,
                "zero": n == 0,
                "positive": n >= 1,
            }[claim],
            "claimed_result": sequence_claim(n),
            "canonical_result": canonical(n),
            "candidate_result": candidate(n),
        }
    )

loop_witnesses = [
    {
        "N": 0,
        "I": 1,
        "J": 7,
        "result_binding": "0",
    },
    {
        "N": 5,
        "I": 3,
        "J": -99,
        "result_binding": "0 1 2",
    },
]
for witness in loop_witnesses:
    n = witness["N"]
    i = witness["I"]
    witness["formal_precondition_satisfied"] = (
        i >= 1
        and (n == 0 or n >= 1)
        and (i == n + 1 or i < n + 1)
    )
    witness["binding_matches_sequenceCodes_I_minus_1"] = (
        witness["result_binding"] == sequence_claim(i - 1)
    )
    witness["claimed_final_result"] = sequence_claim(n)
    witness["canonical_final_result"] = canonical(n)
    witness["candidate_final_result"] = candidate(n)

payload = {"entry_witnesses": entries, "loop_witnesses": loop_witnesses}
print(json.dumps(payload, indent=2, sort_keys=True))

checks = [
    row["formal_precondition_satisfied"]
    and row["claimed_result"]
    == row["canonical_result"]
    == row["candidate_result"]
    for row in entries
]
checks += [
    row["formal_precondition_satisfied"]
    and row["binding_matches_sequenceCodes_I_minus_1"]
    and row["claimed_final_result"]
    == row["canonical_final_result"]
    == row["candidate_final_result"]
    for row in loop_witnesses
]
raise SystemExit(0 if all(checks) else 1)
