#!/usr/bin/env python3
"""Independent differential audit for HumanEval/59."""

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.largest_prime_factor


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--solution", type=Path, required=True)
    parser.add_argument("--inputs-out", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_function(args.canonical, "trusted_humaneval59_canonical")
    generated = load_function(args.solution, "audited_humaneval59_solution")

    documented = [13195, 2048]
    boundary = [4]  # smallest input satisfying the prompt's composite domain
    branch = [6, 8, 9, 15, 21, 25, 49, 77, 121, 143, 221]
    exhaustive = [n for n in range(4, 5001) if not is_prime(n)]
    representative = [
        2 * 5003,
        3 * 3253,
        17 * 509,
        97 * 101,
        2**14,
        3**9,
        5**7,
    ]
    claim_only_prime_boundary = [2, 3, 5, 97]

    intended_inputs = sorted(
        set(documented + boundary + branch + exhaustive + representative)
    )
    extended_inputs = intended_inputs + claim_only_prime_boundary
    records = []
    mismatches = []
    for n in extended_inputs:
        expected = canonical(n)
        actual = generated(n)
        in_prompt_domain = n > 1 and not is_prime(n)
        record = {
            "n": n,
            "canonical": expected,
            "generated": actual,
            "prompt_domain": in_prompt_domain,
        }
        records.append(record)
        if actual != expected:
            mismatches.append(record)

    payload = {
        "documented": documented,
        "boundary": boundary,
        "branch": branch,
        "exhaustive_composites_4_through_5000": exhaustive,
        "representative_generated_composites": representative,
        "claim_only_prime_boundary": claim_only_prime_boundary,
        "records": records,
    }
    args.inputs_out.write_text(json.dumps(payload, indent=2) + "\n")
    digest = hashlib.sha256(args.inputs_out.read_bytes()).hexdigest()

    print("contract_empty_case=not_applicable_scalar_integer_domain")
    print(f"prompt_domain_cases={len(intended_inputs)}")
    print(f"claim_only_prime_cases={len(claim_only_prime_boundary)}")
    print(f"total_cases={len(extended_inputs)}")
    print(f"inputs_sha256={digest}")
    print(f"mismatches={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches[:20], sort_keys=True))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
