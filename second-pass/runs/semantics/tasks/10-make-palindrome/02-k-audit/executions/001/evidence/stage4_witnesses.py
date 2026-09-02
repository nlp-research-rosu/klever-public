#!/usr/bin/env python3
"""Ground witnesses for the submitted helper and loop reachability claims."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def palindrome_from(value: str, start: int) -> str:
    for index in range(start, len(value)):
        suffix = value[index:]
        if suffix == suffix[::-1]:
            return value + value[:index][::-1]
    return value


def main() -> int:
    canonical = load_module("trusted_canonical", Path("/reference/canonical.py"))
    candidate = load_module(
        "audited_candidate",
        Path("/tmp/audit-work/palindrome-audit/candidate/solution.py"),
    )

    helper_value = "cat"
    helper = {
        "claim": "helper-body claim at spec.k:8",
        "substitution": {
            "S": [ord(char) for char in helper_value],
            "L0": 1,
            "CALLER0": 0,
            "REST0": {},
            "STACK0": [],
            "HH": {},
            "NN": 0,
        },
        "precondition": {
            "L0_gt_0": 1 > 0,
            "L0_not_in_REST0": 1 not in {},
        },
        "claimed_palindromeIS": helper_value == helper_value[::-1],
        "canonical_is_palindrome": canonical.is_palindrome(helper_value),
        "candidate_is_palindrome": candidate.is_palindrome(helper_value),
    }

    loop_value = "cat"
    loop_start = 0
    loop = {
        "claim": "loop-fragment claim at spec.k:30",
        "substitution": {
            "S": [ord(char) for char in loop_value],
            "I": loop_start,
            "L": 1,
            "J": 0,
            "CALLER": 0,
            "REST": [],
            "H": {},
            "N": 0,
        },
        "precondition": {
            "zero_le_I": 0 <= loop_start,
            "I_le_isLen_S": loop_start <= len(loop_value),
            "L_gt_0": 1 > 0,
        },
        "claimed_palindromeFrom": palindrome_from(loop_value, loop_start),
        "canonical_make_palindrome": canonical.make_palindrome(loop_value),
        "candidate_make_palindrome": candidate.make_palindrome(loop_value),
    }

    boundary_value = ""
    boundary = {
        "claim": "same loop-fragment claim at its I == isLen(S) boundary",
        "substitution": {
            "S": [],
            "I": 0,
            "L": 1,
            "J": 0,
            "CALLER": 0,
            "REST": [],
            "H": {},
            "N": 0,
        },
        "precondition": {
            "zero_le_I": True,
            "I_le_isLen_S": True,
            "L_gt_0": True,
        },
        "claimed_palindromeFrom": palindrome_from(boundary_value, 0),
        "canonical_make_palindrome": canonical.make_palindrome(boundary_value),
        "candidate_make_palindrome": candidate.make_palindrome(boundary_value),
    }

    record = {"helper_witness": helper, "loop_witness": loop, "boundary": boundary}
    print(json.dumps(record, ensure_ascii=False, indent=2))

    checks = [
        *helper["precondition"].values(),
        helper["claimed_palindromeIS"] == helper["canonical_is_palindrome"],
        helper["claimed_palindromeIS"] == helper["candidate_is_palindrome"],
        *loop["precondition"].values(),
        loop["claimed_palindromeFrom"] == loop["canonical_make_palindrome"],
        loop["claimed_palindromeFrom"] == loop["candidate_make_palindrome"],
        *boundary["precondition"].values(),
        boundary["claimed_palindromeFrom"] == boundary["canonical_make_palindrome"],
        boundary["claimed_palindromeFrom"] == boundary["candidate_make_palindrome"],
    ]
    print(f"all_witness_checks_pass={all(checks)}")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
