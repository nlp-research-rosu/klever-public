#!/usr/bin/env python3
"""Check lexical program pinning and satisfying ground claim witnesses."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path


ROOT = Path("/tmp/audit-work/47-median")
PROGRAM = ROOT / "candidate-src/solution.mpy"
SPEC = ROOT / "candidate-src/spec.k"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.median


def outcome(fn, values: list[int]):
    try:
        value = fn(values.copy())
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))
    return ("return", type(value).__name__, repr(value))


def main() -> int:
    normalize = lambda text: re.sub(
        r"\s+", "", re.sub(r"//.*", "", text, flags=re.MULTILINE)
    )
    program_term = normalize(PROGRAM.read_text(encoding="utf-8"))
    spec_text = normalize(SPEC.read_text(encoding="utf-8"))
    occurrence_count = spec_text.count(program_term)
    print(f"NORMALIZED_PROGRAM_OCCURRENCES_IN_SPEC {occurrence_count}")

    partition_ok = True
    for split_name in [
        "spec-main-only.k",
        "spec-example-odd-only.k",
        "spec-example-even-only.k",
    ]:
        split_text = normalize(
            (ROOT / "candidate-src" / split_name).read_text(encoding="utf-8")
        )
        claim_text = split_text.split("claim", 1)[1].rsplit("endmodule", 1)[0]
        split_count = spec_text.count("claim" + claim_text)
        partition_ok = partition_ok and split_count == 1
        print(f"SPLIT_CLAIM_OCCURRENCES_IN_ORIGINAL {split_name} {split_count}")

    candidate = load(ROOT / "candidate-src/solution.py", "stage4_candidate")
    canonical = load(ROOT / "trusted/canonical.py", "stage4_canonical")

    # Each entry is a satisfiable ground state for the corresponding claim.
    witnesses = [
        {
            "claim": "universal-main",
            "input": [1, 2, 3, 4],
            "precondition": "len(input) >= 3",
            "precondition_holds": True,
            "claimed_k_result": "floatVal(7, 2)",
        },
        {
            "claim": "prompt-odd-example",
            "input": [3, 1, 2, 4, 5],
            "precondition": "true",
            "precondition_holds": True,
            "claimed_k_result": "intVal(3)",
        },
        {
            "claim": "prompt-even-example",
            "input": [-10, 4, 6, 1000, 10, 20],
            "precondition": "true",
            "precondition_holds": True,
            "claimed_k_result": "floatVal(30, 2)",
        },
    ]
    for witness in witnesses:
        values = witness["input"]
        witness["candidate_python"] = outcome(candidate, values)
        witness["canonical_python"] = outcome(canonical, values)
        print("WITNESS " + json.dumps(witness, sort_keys=True))

    return 0 if occurrence_count == 3 and partition_ok else 1


if __name__ == "__main__":
    sys.exit(main())
