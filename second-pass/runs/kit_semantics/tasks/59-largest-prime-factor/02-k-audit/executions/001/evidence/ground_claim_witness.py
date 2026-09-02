#!/usr/bin/env python3
"""Ground witnesses for the entry and loop claim preconditions/results."""

import importlib.util
import json
from pathlib import Path


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.largest_prime_factor


def lpf_from(n: int, factor: int):
    trace = []
    while True:
        trace.append({"n": n, "factor": factor})
        if n <= factor:
            return n, trace
        if n % factor == 0:
            n = n // factor
        else:
            factor += 1


def main() -> int:
    canonical = load("/reference/canonical.py", "witness_canonical")
    solution = load("/tmp/audit-work/h59/solution.py", "witness_solution")
    witnesses = []
    for n, factor in ((4, 2), (15, 2), (13195, 2), (2048, 2)):
        summary, trace = lpf_from(n, factor)
        row = {
            "n": n,
            "factor": factor,
            "entry_precondition": n >= 2,
            "loop_precondition": factor >= 2,
            "lpfFrom": summary,
            "canonical": canonical(n),
            "solution": solution(n),
            "summary_trace": trace,
        }
        assert row["entry_precondition"] and row["loop_precondition"]
        assert summary == row["canonical"] == row["solution"]
        witnesses.append(row)
    print(json.dumps(witnesses, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
