#!/usr/bin/env python3
"""Ground witnesses for claim satisfiability and result substitution."""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path


def load_function(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.special_factorial


def claimed_special_factorial(n: int) -> int:
    # Ground interpretation of verification.k's equations:
    # specialFactorial(n) = specialFactorial(n-1) * factorial(n), base 1.
    return math.prod(math.factorial(i) for i in range(1, n + 1))


def main() -> int:
    canonical = load_function(Path("/reference/canonical.py"), "stage4_canonical")
    submitted = load_function(
        Path("/tmp/audit-work/139-special-factorial/solution.py"),
        "stage4_submitted",
    )
    values = [1, 2, 4, 6, 10]
    failures = []
    print(
        "entry_witness: N=4; N>0; initial <k> is the spec's #loadAll term; "
        "<env>=0; scopes={0: scope({},parent(-1)),-1:builtinsScope}; "
        "scopeLoc=1; heap={}; heapLoc=0; stack=[]; ret=noRet; exc=NoExc; exit-code=0"
    )
    print(
        "loop_witness: N=4,I=1,L=1,SC contains module scope 0; "
        "local scope={n:4,factorial:factorial(0)=1,"
        "result:specialFactorial(0)=1,i:1,parent(0)}"
    )
    for n in values:
        precondition = n > 0
        claimed = claimed_special_factorial(n)
        oracle = canonical(n)
        subject = submitted(n)
        print(
            f"N={n} precondition={precondition} "
            f"claimed={claimed} canonical={oracle} submitted={subject}"
        )
        if not precondition or claimed != oracle or claimed != subject:
            failures.append(n)
    print(f"failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
