#!/usr/bin/env python3
"""Ground witnesses for each candidate claim precondition and claimed result."""

from __future__ import annotations

import importlib.util
from pathlib import Path


WORK = Path("/tmp/audit-work/31-is-prime-audit")


def import_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def trial_prime(n: int, divisor: int) -> bool:
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 1
    return True


def main() -> int:
    canonical = import_module(WORK / "canonical.py", "claim_canonical")
    submitted = import_module(WORK / "solution.py", "claim_submitted")

    loop_n, loop_d, loop_l = 5, 2, 1
    loop_pre = (
        loop_d >= 2
        and loop_l != 0
        and 0 not in {}
        and loop_l not in {}
    )
    loop_claimed = trial_prime(loop_n, loop_d)
    print(
        "LOOP_WITNESS: "
        "N=5 D=2 L=1 CALLER=0 SC={} GLOBAL=scope({},root) "
        "H={} HL=0 CONT=.K STACK=.List"
    )
    print(f"LOOP_PRECONDITION_SATISFIED={loop_pre}")
    print(
        f"LOOP_CLAIMED_RESULT={loop_claimed} "
        f"canonical={canonical.is_prime(loop_n)} "
        f"submitted={submitted.is_prime(loop_n)}"
    )

    small_n = 1
    print(
        "ENTRY_SMALL_WITNESS: "
        "N=1 B=builtinsScope CONT=.K with exact closure/body and call frame"
    )
    print(f"ENTRY_SMALL_PRECONDITION_SATISFIED={small_n < 2}")
    print(
        f"ENTRY_SMALL_CLAIMED_RESULT=False "
        f"canonical={canonical.is_prime(small_n)} "
        f"submitted={submitted.is_prime(small_n)}"
    )

    for large_n in (4, 5):
        print(
            "ENTRY_LARGE_PREFIX_WITNESS: "
            f"N={large_n} SC={{}} env=1 scope[1]={{n:{large_n}}}"
        )
        print(
            "ENTRY_LARGE_PREFIX_PRECONDITION_SATISFIED="
            f"{large_n >= 2 and 1 not in {}}"
        )
        print(
            "ENTRY_LARGE_PREFIX_CLAIMED_RHS="
            "Assign(divisor,2); While(...); Return(true); #endcall "
            "(a residual computation, not a Bool)"
        )
        print(
            f"ENTRY_LARGE_DESIRED_RESULT canonical={canonical.is_prime(large_n)} "
            f"submitted={submitted.is_prime(large_n)}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
