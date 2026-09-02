#!/usr/bin/env python3
"""Independent differential oracle for HumanEval 39 prime_fib."""

from __future__ import annotations

import importlib.util
import json
import multiprocessing
import random
from pathlib import Path
from types import ModuleType
from typing import Callable


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def child_call(fn: Callable[[int], int], n: int, queue) -> None:
    try:
        queue.put({"kind": "return", "value": fn(n)})
    except BaseException as err:  # Evidence records any actual boundary behavior.
        queue.put({"kind": "exception", "type": type(err).__name__, "text": str(err)})


def bounded_call(fn: Callable[[int], int], n: int, timeout_s: float = 0.25) -> dict:
    ctx = multiprocessing.get_context("fork")
    queue = ctx.Queue()
    proc = ctx.Process(target=child_call, args=(fn, n, queue))
    proc.start()
    proc.join(timeout_s)
    if proc.is_alive():
        proc.terminate()
        proc.join()
        return {"kind": "timeout", "timeout_s": timeout_s}
    if not queue.empty():
        return queue.get()
    return {"kind": "no-result", "exitcode": proc.exitcode}


def main() -> int:
    canonical_mod = load_module("trusted_canonical", Path("/reference/canonical.py"))
    generated_mod = load_module("generated_solution", Path("/tmp/audit-work/solution.py"))
    canonical = canonical_mod.prime_fib
    generated = generated_mod.prime_fib

    examples = {1: 2, 2: 3, 3: 5, 4: 13, 5: 89}
    # 1/2 exercise b < 2 and zero-iteration divisor loops; 3 exercises the
    # non-divisor branch; 4+ exercise composite/divisor and later prime paths.
    branch_and_boundary = list(range(1, 11))
    rng = random.Random(39039)
    representative_generated = [rng.randint(1, 10) for _ in range(12)]
    intended_inputs = sorted(set(examples) | set(branch_and_boundary) | set(representative_generated))

    rows = []
    mismatches = 0
    for n in intended_inputs:
        expected = canonical(n)
        actual = generated(n)
        match = expected == actual
        mismatches += not match
        rows.append({"n": n, "canonical": expected, "generated": actual, "match": match})
        if n in examples and expected != examples[n]:
            raise AssertionError((n, expected, examples[n]))

    boundary = {
        "domain_note": "n=0 is outside the documented positive ordinal domain",
        "n=0": {
            "canonical": bounded_call(canonical, 0),
            "generated": bounded_call(generated, 0),
        },
    }

    report = {
        "documented_examples": examples,
        "branch_and_boundary_inputs": branch_and_boundary,
        "representative_seed": 39039,
        "representative_generated_inputs": representative_generated,
        "intended_domain_rows": rows,
        "intended_domain_mismatch_count": mismatches,
        "out_of_domain_boundary": boundary,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
