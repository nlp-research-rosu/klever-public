#!/usr/bin/env python3
"""Concrete satisfiability and claimed-result substitution witness."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path):
    spec = importlib.util.spec_from_file_location(f"ground_{path.stem}_{id(path)}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_positive


def main() -> int:
    witness = [-1, 0, 2, 0.5, -3.25]
    precondition = all(type(value) in {int, float} for value in witness)
    positivity_atoms = [value > 0.0 for value in witness]
    instantiated_claim_result = [
        value for value, is_positive in zip(witness, positivity_atoms) if is_positive
    ]
    canonical_result = load(Path("/reference/canonical.py"))(list(witness))
    generated_result = load(Path("/candidate/solution.py"))(list(witness))
    k_vs = (
        "vCons(-1, vCons(0, vCons(2, "
        "vCons(0.5, vCons(-3.25, .ValSeq)))))"
    )

    print(f"WITNESS={witness!r}")
    print(f"ENTRY_PRECONDITION_numericVals={precondition}")
    print(f"K_SUBSTITUTION_VS={k_vs}")
    print(f"POSITIVE_NUMERIC_ATOMS={positivity_atoms}")
    print(
        "INSTANTIATED_POST="
        f"ref(0), heap[0]=list({instantiated_claim_result!r})"
    )
    print(f"CANONICAL_RESULT={canonical_result!r}")
    print(f"GENERATED_RESULT={generated_result!r}")
    equal = (
        precondition
        and instantiated_claim_result == canonical_result == generated_result
    )
    print(f"ALL_EQUAL={equal}")
    return int(not equal)


if __name__ == "__main__":
    raise SystemExit(main())
