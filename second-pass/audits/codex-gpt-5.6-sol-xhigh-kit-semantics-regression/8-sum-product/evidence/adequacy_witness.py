#!/usr/bin/env python3
"""Concrete satisfying witnesses for both positive reachability claims."""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path
from types import ModuleType


def load(name: str, path: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def folds(values: list[int], initial_sum: int, initial_product: int) -> tuple[int, int]:
    return initial_sum + sum(values), initial_product * math.prod(values)


def main() -> None:
    canonical = load("trusted_canonical_witness", "/tmp/audit-work/trusted/canonical.py")
    candidate = load("candidate_witness", "/tmp/audit-work/src/solution.py")

    print("ENTRY CLAIM SATISFYING STATE")
    print("VS=.ValSeq; env=0; scopes=(-1|->builtinsScope, 0|->empty root scope)")
    print("scopeLoc=1; heap=.Map; heapLoc=0; stack=.List; noRet; NoExc; exit-code=0")
    print("intsVS(.ValSeq)=true")
    print(f"formal_folds={folds([], 0, 1)}")
    print(f"canonical={canonical.sum_product([])}")
    print(f"candidate={candidate.sum_product([])}")

    entry_values = [2, 4]
    print("\nENTRY NONEMPTY SUBSTITUTION")
    print("VS=vCons(2,vCons(4,.ValSeq)); remaining cells as above")
    print(f"formal_folds={folds(entry_values, 0, 1)}")
    print(f"canonical={canonical.sum_product(entry_values)}")
    print(f"candidate={candidate.sum_product(entry_values)}")

    print("\nLOOP CLAIM SATISFYING AND REACHABLE STATE")
    print("VS=INPUT=vCons(2,vCons(4,.ValSeq)); T=0; P=1; N=0")
    print("env=1; scopeLoc=2; heap=.Map; heapLoc=0")
    print("stack=ListItem(frame(.K,0,1)); noRet; NoExc; exit-code=0")
    print("the closure body and trailing Return(... ) ~> #endcall are exactly as in spec.k")
    print("intsVS(VS)=true")
    print(f"formal_folds={folds(entry_values, 0, 1)}")
    print("expected K result=tuple(vCons(6,vCons(8,.ValSeq)))")

    assert folds([], 0, 1) == canonical.sum_product([]) == candidate.sum_product([])
    assert (
        folds(entry_values, 0, 1)
        == canonical.sum_product(entry_values)
        == candidate.sum_product(entry_values)
        == (6, 8)
    )
    print("\nADEQUACY_WITNESSES=PASS")


if __name__ == "__main__":
    main()
