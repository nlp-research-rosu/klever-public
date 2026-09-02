#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.starts_one_ends


def main() -> int:
    if len(sys.argv) != 3:
        return 2
    trusted = load_entry("trusted_mutation_witness", Path(sys.argv[1]))
    candidate = load_entry("candidate_mutation_witness", Path(sys.argv[2]))
    n = 3
    false_target = 181
    trusted_value = trusted(n)
    candidate_value = candidate(n)
    print(f"n = {n}")
    print(f"multi_digit_precondition_n_gt_1 = {n > 1}")
    print(f"trusted_value = {trusted_value}")
    print(f"candidate_value = {candidate_value}")
    print(f"false_mutated_target = {false_target}")
    print(
        "mutation_demonstrably_false = "
        f"{trusted_value == candidate_value and candidate_value != false_target}"
    )
    return 0 if trusted_value == candidate_value and candidate_value != false_target else 1


if __name__ == "__main__":
    raise SystemExit(main())
