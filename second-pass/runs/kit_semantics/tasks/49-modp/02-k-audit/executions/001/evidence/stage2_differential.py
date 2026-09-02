#!/usr/bin/env python3

"""Independent differential checks for HumanEval/49 modp."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from pathlib import Path
from typing import Callable


SCRATCH = Path("/tmp/audit-work/49-modp")


def load_function(module_name: str, path: Path) -> Callable[[int, int], object]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.modp


canonical = load_function("trusted_canonical_modp", SCRATCH / "trusted-canonical.py")
generated = load_function("generated_solution_modp", SCRATCH / "solution.py")


def outcome(function: Callable[[int, int], object], n: int, p: int) -> tuple[str, str, str]:
    try:
        value = function(n, p)
        return ("return", type(value).__name__, repr(value))
    except Exception as err:  # Deliberately compare observable exception class.
        return ("raise", type(err).__name__, str(err))


examples = [(3, 5), (1101, 101), (0, 101), (3, 11), (100, 101)]
branch_boundaries = [
    (n, p)
    for n in (-3, -1, 0, 1, 2, 3)
    for p in (-5, -2, -1, 0, 1, 2, 5)
]
systematic = [(n, p) for n in range(-5, 65) for p in range(-20, 21)]
large = [(1101, p) for p in (-101, -5, -1, 1, 5, 101)] + [
    (10000, p) for p in (-101, -5, -1, 1, 5, 101)
]
rng = random.Random(49049)
generated_cases = [(rng.randint(-8, 512), rng.randint(-128, 128)) for _ in range(2000)]
all_cases = sorted(set(examples + branch_boundaries + systematic + large + generated_cases))


def mismatches(cases: list[tuple[int, int]]) -> list[dict[str, object]]:
    result = []
    for n, p in cases:
        expected = outcome(canonical, n, p)
        actual = outcome(generated, n, p)
        if expected != actual:
            result.append(
                {"n": n, "p": p, "canonical": expected, "generated": actual}
            )
    return result


subsets = {
    "documented_examples": examples,
    "canonical_loop_branch_boundaries": branch_boundaries,
    "mathematically_defined_claim_domain_n_ge_0_p_ne_0": [
        case for case in all_cases if case[0] >= 0 and case[1] != 0
    ],
    "usual_nonnegative_positive_modulus_domain": [
        case for case in all_cases if case[0] >= 0 and case[1] > 0
    ],
    "all_typed_integer_sample_including_undefined_or_negative_cases": all_cases,
}

encoded_inputs = json.dumps(all_cases, separators=(",", ":")).encode()
print("oracle=/tmp/audit-work/49-modp/trusted-canonical.py::modp")
print("generated=/tmp/audit-work/49-modp/solution.py::modp")
print("random_seed=49049")
print("systematic_n=-5..64")
print("systematic_p=-20..20")
print("generated_random_cases=2000 with n=-8..512 and p=-128..128")
print(f"distinct_total_cases={len(all_cases)}")
print(f"inputs_sha256={hashlib.sha256(encoded_inputs).hexdigest()}")

results: dict[str, list[dict[str, object]]] = {}
for name, cases in subsets.items():
    differing = mismatches(cases)
    results[name] = differing
    print(f"{name}: cases={len(cases)} mismatches={len(differing)}")
    for witness in differing[:12]:
        print("WITNESS " + json.dumps(witness, sort_keys=True))
    if len(differing) > 12:
        print(f"WITNESSES_OMITTED={len(differing) - 12}")

# The documented examples and the mathematically defined target domain must agree.
required = (
    results["documented_examples"]
    + results["mathematically_defined_claim_domain_n_ge_0_p_ne_0"]
)
raise SystemExit(1 if required else 0)
