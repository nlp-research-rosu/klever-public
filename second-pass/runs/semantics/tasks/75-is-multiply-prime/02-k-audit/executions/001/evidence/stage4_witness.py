#!/usr/bin/env python3
"""Ground witnesses for the symbolic and concrete entry claims."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/75-prime")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    canonical = load("canonical_witness", SCRATCH / "trusted" / "canonical.py")
    generated = load("generated_witness", SCRATCH / "candidate" / "solution.py")
    expected = {-7: False, 0: False, 75: True}
    rows = []
    for value, claimed in expected.items():
        canonical_result = canonical.is_multiply_prime(value)
        generated_result = generated.is_multiply_prime(value)
        rows.append(
            {
                "input": value,
                "claim_expected": claimed,
                "canonical": canonical_result,
                "generated": generated_result,
                "all_equal": claimed == canonical_result == generated_result,
            }
        )
    print(
        json.dumps(
            {
                "symbolic_precondition_witness": (
                    "A=-7 with the exact initial cells written in SPEC-NEGATIVE; "
                    "-7 < 2"
                ),
                "concrete_true_claim_witness": (
                    "A=75 with the exact initial cells written in SPEC-72-81"
                ),
                "results": rows,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if all(row["all_equal"] for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
