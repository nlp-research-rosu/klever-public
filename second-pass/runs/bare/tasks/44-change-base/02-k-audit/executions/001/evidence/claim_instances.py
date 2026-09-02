#!/usr/bin/env python3
"""Ground instances of the formal pre/postcondition compared with both programs."""

from __future__ import annotations

import importlib.util
import pathlib
from typing import Callable


def load_entry(path: pathlib.Path, module_name: str) -> Callable[[int, int], str]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.change_base


def formal_base_string(x: int, base: int) -> str:
    if x < base:
        return str(x)
    return formal_base_string(x // base, base) + str(x % base)


def main() -> int:
    candidate = load_entry(
        pathlib.Path("/tmp/audit-work/44-change-base.Cjtazd/candidate-src/solution.py"),
        "candidate_claim_instance",
    )
    canonical = load_entry(
        pathlib.Path("/reference/canonical.py"), "canonical_claim_instance"
    )
    for x, base in ((8, 3), (0, 2), (2, 2), (1234, 7)):
        precondition = 0 <= x and 2 <= base <= 9
        formal_result = formal_base_string(x, base)
        candidate_result = candidate(x, base)
        canonical_result = canonical(x, base)
        print(
            f"X={x} B={base} PRE={precondition} "
            f"FORMAL_POST={formal_result!r} CANDIDATE={candidate_result!r} "
            f"CANONICAL={canonical_result!r} "
            f"FORMAL_EQ_CANDIDATE={formal_result == candidate_result} "
            f"FORMAL_EQ_CANONICAL={formal_result == canonical_result}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
