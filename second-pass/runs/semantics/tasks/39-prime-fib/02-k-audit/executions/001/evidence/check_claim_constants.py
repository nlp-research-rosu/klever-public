#!/usr/bin/env python3
"""Extract every entry claim and compare its ground result with both Pythons."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path


SPEC = Path("/candidate/spec.k")


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    text = SPEC.read_text()
    pattern = re.compile(
        r"claim \[(pf\d+)\]:\s*"
        r'<k> Call\(Name\("prime_fib"\), Int\((\d+)\)\) => (\d+) </k>'
    )
    claims = [(label, int(n), int(result)) for label, n, result in pattern.findall(text)]
    canonical = load("claim_canonical", "/reference/canonical.py")
    generated = load("claim_generated", "/candidate/solution.py")
    print(f"ENTRY_CLAIMS={len(claims)}")
    print(
        "SATISFYING_STATE_TEMPLATE="
        "k=Call(Name(\"prime_fib\"),Int(n)); env=0; "
        "scopes={0:{_is_prime:isPrimeClosure,prime_fib:primeFibClosure,parent=-1},"
        "-1:builtinsScope}; scopeLoc=1; heap={}; heapLoc=0; stack=[]; "
        "ret=noRet; exc=NoExc; exit-code=0"
    )
    mismatches = 0
    for label, n, claimed in claims:
        canonical_value = canonical.prime_fib(n)
        generated_value = generated.prime_fib(n)
        okay = claimed == canonical_value == generated_value
        print(
            f"{label} n={n} claimed={claimed} canonical={canonical_value} "
            f"generated={generated_value} all_equal={okay}"
        )
        mismatches += not okay
    print(f"MISMATCHES={mismatches}")
    return 1 if len(claims) != 11 or mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
