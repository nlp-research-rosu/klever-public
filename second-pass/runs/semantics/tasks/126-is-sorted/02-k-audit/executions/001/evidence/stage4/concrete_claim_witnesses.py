#!/usr/bin/env python3
"""Ground instances of the K scan postcondition versus both Python functions."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_sorted


def scan_result(ok: bool, previous: int, count: int, values: list[int]) -> bool:
    for value in values:
        next_count = count + 1 if value == previous else 1
        ok = ok and previous <= value and next_count <= 2
        previous = value
        count = next_count
    return ok


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} CANONICAL.py SOLUTION.py", file=sys.stderr)
        return 64
    canonical = load_function(Path(sys.argv[1]), "witness_canonical")
    generated = load_function(Path(sys.argv[2]), "witness_generated")

    in_domain = [
        [],
        [0],
        [0, 0],
        [0, 0, 0],
        [1, 2, 2, 3],
        [1, 3, 2],
        [4, 4],
        [4, 4, 4],
    ]
    mismatches = 0
    for values in in_domain:
        k_post = scan_result(True, 0, 0, values)
        canon = canonical(list(values))
        actual = generated(list(values))
        print(f"entry INPUT={values}: K_post={k_post} canonical={canon} generated={actual}")
        mismatches += not (k_post == canon == actual)

    # Satisfies the loop claim's arithmetic/map side conditions with:
    # FRAME=SAVED=1, CALLER=0, CURRENT=2, LOCALS=.Map, BASE containing only
    # frames 0 and -1, NUMBER=1, OK=true, PREV=1, COUNT=1.
    loop_suffix = [2, 2]
    loop_post = scan_result(True, 1, 1, loop_suffix)
    print(
        "loop witness: OK=true PREV=1 COUNT=1 IS=[2,2] "
        f"=> scanResult(scanAll(...))={loop_post}"
    )

    off_domain = [-1]
    print(
        f"off-domain INPUT={off_domain}: "
        f"K_post={scan_result(True, 0, 0, off_domain)} "
        f"canonical={canonical(off_domain)} generated={generated(off_domain)}"
    )
    print(f"in_domain_mismatches={mismatches}")
    return 0 if mismatches == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
