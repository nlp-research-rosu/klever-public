#!/usr/bin/env python3
"""Finite check of the K baseDigits equations against the trusted canonical."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_canonical():
    path = Path("/reference/canonical.py")
    spec = importlib.util.spec_from_file_location("summary_oracle", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.change_base


def base_digits_equations(x: int, base: int) -> str:
    # Iterative evaluation of:
    # baseDigits(0,B)=empty;
    # baseDigits(N,B)=baseDigits(N//B,B) ++ [48 + N%B].
    codes = []
    while x > 0:
        quotient, remainder = divmod(x, base)
        codes.append(48 + remainder)
        x = quotient
    return "".join(chr(code) for code in reversed(codes))


def main() -> int:
    canonical = load_canonical()
    cases = [(x, base) for base in range(2, 10) for x in range(0, 4097)]
    rng = random.Random(441337)
    for _ in range(512):
        cases.append((rng.getrandbits(rng.randint(0, 4096)), rng.randint(2, 9)))

    mismatches = []
    for x, base in cases:
        expected = canonical(x, base)
        actual = base_digits_equations(x, base)
        if expected != actual:
            mismatches.append((x, base, expected, actual))

    print("SUMMARY=verification.k baseDigits recurrence")
    print("ORACLE=/reference/canonical.py:change_base")
    print(
        "SCOPE=all x=0..4096/base=2..9 plus "
        "512 deterministic generated integers up to 4096 bits (seed 441337)"
    )
    print(f"TOTAL_CASES={len(cases)}")
    print(f"MISMATCHES={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print(f"MISMATCH={mismatch!r}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
