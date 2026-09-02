#!/usr/bin/env python3
"""Independent differential test for HumanEval 113 odd_count.

The canonical implementation comes only from /reference/canonical.py.  The
generated implementation comes only from the fresh scratch copy.  The corpus
contains the documented examples, explicit empty/boundary/branch cases,
exhaustive singleton inputs for every digit string of length 0..3, structured
multi-element inputs, and fixed-seed generated lists.
"""

import hashlib
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/audit-113/solution.py")
INPUT_RECORD = Path("/audit-output/evidence/02_differential_inputs.json")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_cases():
    cases = [
        ["1234567"],
        ["3", "11111111"],
        [],
        [""],
        ["0"],
        ["1"],
        ["2"],
        ["9"],
        ["01"],
        ["10"],
        ["24680"],
        ["13579"],
        ["0123456789"],
        ["0000000000"],
        ["9999999999"],
        ["24680", "13579", ""],
        ["1" * 1000],
        ["0" * 1000],
        ["0123456789" * 100],
    ]

    digits = "0123456789"
    for length in range(4):
        for chars in itertools.product(digits, repeat=length):
            cases.append(["".join(chars)])

    cases.extend(
        [
            ["", "0", "1", "2", "9"],
            ["00", "11", "22", "99"],
            ["123", "456", "789", "012"],
        ]
    )

    rng = random.Random(113)
    for _ in range(500):
        list_length = rng.randrange(0, 9)
        cases.append(
            [
                "".join(rng.choice(digits) for _ in range(rng.randrange(0, 41)))
                for _ in range(list_length)
            ]
        )
    return cases


def main() -> int:
    canonical = load_module("trusted_canonical", CANONICAL_PATH)
    generated = load_module("fresh_generated", GENERATED_PATH)
    cases = build_cases()

    serialized = json.dumps(cases, ensure_ascii=True, separators=(",", ":"))
    INPUT_RECORD.write_text(serialized + "\n", encoding="utf-8")
    digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    mismatches = []
    for index, value in enumerate(cases):
        expected = canonical.odd_count(value)
        actual = generated.odd_count(value)
        if actual != expected:
            mismatches.append(
                {
                    "index": index,
                    "input": value,
                    "canonical": expected,
                    "generated": actual,
                }
            )

    print(f"canonical={CANONICAL_PATH}")
    print(f"generated={GENERATED_PATH}")
    print("formal_test_domain=list[str] where every character is an ASCII decimal digit")
    print("exhaustive_singleton_strings=all digit strings of length 0..3")
    print("fixed_seed_generated_lists=500 seed=113 max_list_length=8 max_string_length=40")
    print(f"total_cases={len(cases)}")
    print(f"serialized_inputs_sha256={digest}")
    print(f"input_record={INPUT_RECORD}")
    print(f"mismatch_count={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches[:20], indent=2, sort_keys=True))
        return 1
    print("RESULT=ZERO_MISMATCHES")
    return 0


if __name__ == "__main__":
    sys.exit(main())
