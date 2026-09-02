#!/usr/bin/env python3
"""Independent differential test for HumanEval/76.

The oracle is the trusted mounted canonical.py.  The generated implementation is
the clean scratch copy of candidate solution.py.  The deterministic generated
grid deliberately includes negative bases because neither the trusted prompt nor
the canonical signature restricts the integer domain to positive bases.
"""

from __future__ import annotations

import importlib.util
import json
import multiprocessing as mp
from pathlib import Path
from typing import Any


CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/76-is-simple-power/solution.py")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def call_worker(path: str, module_name: str, args: tuple[int, int], queue: Any) -> None:
    try:
        fn = load(Path(path), module_name).is_simple_power
        queue.put(("return", fn(*args)))
    except BaseException as err:
        queue.put(("exception", f"{type(err).__name__}: {err}"))


def bounded_call(path: Path, module_name: str, args: tuple[int, int], timeout: float = 0.25):
    queue = mp.Queue()
    process = mp.Process(target=call_worker, args=(str(path), module_name, args, queue))
    process.start()
    process.join(timeout)
    if process.is_alive():
        process.terminate()
        process.join()
        return ("timeout", None)
    if queue.empty():
        return ("child-exit", process.exitcode)
    return queue.get()


canonical = load(CANONICAL_PATH, "trusted_canonical")
generated = load(GENERATED_PATH, "candidate_generated")

documented_examples = [
    (1, 4, True),
    (2, 2, True),
    (8, 2, True),
    (3, 2, False),
    (3, 1, False),
    (5, 3, False),
]

branch_and_boundary_cases = [
    (-1, 2),   # x < 1
    (0, 2),    # x < 1 boundary
    (1, -2),   # x == 1 precedes base handling
    (1, 1),
    (1, 2),
    (2, 1),    # n < 2
    (2, 2),    # n == 2, loop zero iterations
    (3, 2),    # one loop iteration and overshoot
    (4, 2),    # one loop iteration and equality
    (4, -2),   # negative-base even power: known fidelity discriminator
    (8, -2),   # negative-base overshoot
    (16, -2),  # negative-base even power
]

larger_cases = [
    (1024, 2),
    (1000, 10),
    (6561, 3),
    (4096, -2),
    (4095, -2),
    (390625, 5),
]

floating_number_cases = [
    (1.0, -2.5),
    (2.25, 1.5),
    (4.0, 2.0),
    (6.25, 2.5),
    (15.625, 2.5),
]

grid = [(x, n) for x in range(-8, 65) for n in (-5, -4, -3, -2, 1, 2, 3, 4, 5, 6, 7, 8)]

ordered_cases = []
for x, n in branch_and_boundary_cases + larger_cases + floating_number_cases + grid:
    if (x, n) not in ordered_cases:
        ordered_cases.append((x, n))

mismatches = []
for x, n in ordered_cases:
    oracle = canonical.is_simple_power(x, n)
    actual = generated.is_simple_power(x, n)
    if oracle != actual:
        mismatches.append({"x": x, "n": n, "canonical": oracle, "generated": actual})

floating_results = [
    {
        "x": x,
        "n": n,
        "canonical": canonical.is_simple_power(x, n),
        "generated": generated.is_simple_power(x, n),
    }
    for x, n in floating_number_cases
]

example_results = []
for x, n, expected in documented_examples:
    oracle = canonical.is_simple_power(x, n)
    actual = generated.is_simple_power(x, n)
    example_results.append(
        {
            "x": x,
            "n": n,
            "expected": expected,
            "canonical": oracle,
            "generated": actual,
            "all_agree": expected == oracle == actual,
        }
    )

# These canonical calls are nonterminating; isolate them so the audit itself is bounded.
nontermination_probes = []
for args in [(2, 0), (2, -1)]:
    nontermination_probes.append(
        {
            "input": list(args),
            "canonical": bounded_call(CANONICAL_PATH, "canonical_probe", args),
            "generated": bounded_call(GENERATED_PATH, "generated_probe", args),
        }
    )

print(
    json.dumps(
        {
            "oracle": str(CANONICAL_PATH),
            "generated": str(GENERATED_PATH),
            "empty_case": "not applicable: both parameters are scalar numbers",
            "documented_examples": example_results,
            "floating_number_results": floating_results,
            "deterministic_scope": {
                "branch_and_boundary_cases": branch_and_boundary_cases,
                "larger_cases": larger_cases,
                "floating_number_cases": floating_number_cases,
                "generated_grid": {
                    "x": "every integer from -8 through 64 inclusive",
                    "n": [-5, -4, -3, -2, 1, 2, 3, 4, 5, 6, 7, 8],
                },
                "unique_terminating_cases_compared": len(ordered_cases),
            },
            "mismatch_count": len(mismatches),
            "mismatches": mismatches,
            "bounded_nontermination_probes": nontermination_probes,
        },
        indent=2,
        sort_keys=True,
    )
)
