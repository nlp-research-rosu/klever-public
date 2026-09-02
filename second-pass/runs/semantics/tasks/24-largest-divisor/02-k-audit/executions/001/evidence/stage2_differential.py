#!/usr/bin/env python3
"""Independent differential test for HumanEval problem 24.

The intended scalar input domain is integer n > 1.  The trusted HumanEval
implementation and the submitted implementation are loaded from distinct
absolute paths.  An independent divisor-property oracle is also checked.
"""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path
from typing import Any, Callable

CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/solution.py")
INPUTS_PATH = Path("/audit-output/evidence/stage2_inputs.json")


def load_entry(module_name: str, path: Path) -> Callable[[int], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.largest_divisor


def mathematical_oracle(n: int) -> int:
    divisors = [d for d in range(1, n) if n % d == 0]
    return max(divisors)


def outcome(fn: Callable[[int], Any], n: int) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": fn(n)}
    except Exception as err:  # The excluded-domain observation is intentional.
        return {"kind": "raise", "type": type(err).__name__}


canonical = load_entry("trusted_canonical_24", CANONICAL_PATH)
generated = load_entry("submitted_solution_24", GENERATED_PATH)

documented = [15]
boundary_and_branches = [
    2,  # domain minimum; loop guard is false immediately
    3,  # prime; guard true then false at divisor 1
    4,  # composite; guard true then false at divisor 2
    5,
    6,
    8,
    9,
    10,
    12,
    15,
    16,
    25,
    49,
    97,
    100,
    997,
    1024,
    9999,
    10007,
]
exhaustive_small = list(range(2, 2001))
rng = random.Random(240024)
generated_representatives = sorted({rng.randint(2001, 20000) for _ in range(128)})
intended_inputs = sorted(
    set(documented + boundary_and_branches + exhaustive_small + generated_representatives)
)
excluded_inputs = [0, 1]

INPUTS_PATH.write_text(
    json.dumps(
        {
            "intended_domain": "integers n > 1",
            "documented": documented,
            "boundary_and_branches": boundary_and_branches,
            "exhaustive_small": {"start": 2, "stop_inclusive": 2000},
            "generated_seed": 240024,
            "generated_representatives": generated_representatives,
            "intended_inputs_expanded": intended_inputs,
            "excluded_domain_observations": excluded_inputs,
        },
        indent=2,
        sort_keys=True,
    )
    + "\n"
)

mismatches: list[dict[str, Any]] = []
samples: list[dict[str, Any]] = []
for n in intended_inputs:
    expected = canonical(n)
    actual = generated(n)
    property_value = mathematical_oracle(n)
    if n in boundary_and_branches:
        samples.append(
            {
                "n": n,
                "canonical": expected,
                "generated": actual,
                "property_oracle": property_value,
            }
        )
    if expected != actual or expected != property_value:
        mismatches.append(
            {
                "n": n,
                "canonical": expected,
                "generated": actual,
                "property_oracle": property_value,
            }
        )

excluded_observations = [
    {
        "n": n,
        "canonical": outcome(canonical, n),
        "generated": outcome(generated, n),
    }
    for n in excluded_inputs
]

print(f"canonical_path={CANONICAL_PATH}")
print(f"generated_path={GENERATED_PATH}")
print("intended_domain=integers n > 1")
print(f"intended_case_count={len(intended_inputs)}")
print(f"mismatch_count={len(mismatches)}")
print("branch_boundary_samples=" + json.dumps(samples, sort_keys=True))
print(
    "excluded_domain_observations="
    + json.dumps(excluded_observations, sort_keys=True)
)
if mismatches:
    print("mismatches=" + json.dumps(mismatches, sort_keys=True))
    raise SystemExit(1)
