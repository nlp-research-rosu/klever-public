#!/usr/bin/env python3
"""Independent differential test of trusted canonical vs generated solution."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path
from types import ModuleType


ROOT = Path("/tmp/audit-work/120-maximum")


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    canonical = load_module("trusted_canonical", ROOT / "reference" / "canonical.py")
    generated = load_module("generated_solution", ROOT / "candidate" / "solution.py")

    named_cases: list[tuple[str, list[int], int, bool]] = [
        ("example-1", [-3, -4, 5], 3, True),
        ("example-2-duplicate-max", [4, -4, 4], 2, True),
        ("example-3-k-one", [-3, 2, 1, 2, -1, -2, 1], 1, True),
        ("minimum-length-k-zero", [-1000], 0, True),
        ("minimum-length-k-one", [1000], 1, True),
        ("k-zero-unsorted", [7, -1], 0, True),
        ("k-one-boundary", [7, -1], 1, True),
        ("k-equals-length", [7, -1], 2, True),
        ("element-bounds-and-duplicates", [-1000, 1000, -1000, 1000], 3, True),
        ("empty-extension", [], 0, False),
        ("maximum-length-k-zero", list(range(1000, 0, -1)), 0, True),
        ("maximum-length-k-full", list(range(1000, 0, -1)), 1000, True),
    ]

    exhaustive: list[tuple[str, list[int], int, bool]] = []
    alphabet = [-1000, -1, 0, 1, 1000]
    for length in range(1, 6):
        for values in itertools.product(alphabet, repeat=length):
            arr = list(values)
            for k in range(length + 1):
                exhaustive.append((f"exhaustive-len-{length}", arr, k, True))

    rng = random.Random(120)
    random_cases: list[tuple[str, list[int], int, bool]] = []
    for index in range(500):
        length = rng.randint(1, 1000)
        arr = [rng.randint(-1000, 1000) for _ in range(length)]
        k = rng.randint(0, length)
        random_cases.append((f"random-{index}", arr, k, True))

    all_cases = named_cases + exhaustive + random_cases
    result_mismatches: list[dict[str, object]] = []
    post_call_input_mismatches = 0
    serialized_inputs: list[object] = []

    for label, arr, k, intended in all_cases:
        canonical_arg = list(arr)
        generated_arg = list(arr)
        canonical_result = canonical.maximum(canonical_arg, k)
        generated_result = generated.maximum(generated_arg, k)
        serialized_inputs.append([label, arr, k, intended])
        if canonical_result != generated_result:
            result_mismatches.append(
                {
                    "label": label,
                    "arr": arr,
                    "k": k,
                    "canonical": canonical_result,
                    "generated": generated_result,
                }
            )
        if canonical_arg != generated_arg:
            post_call_input_mismatches += 1

    inputs_json = json.dumps(serialized_inputs, separators=(",", ":"), sort_keys=False)
    print(f"named_cases={len(named_cases)}")
    print(f"exhaustive_cases={len(exhaustive)}")
    print(f"random_cases={len(random_cases)} seed=120")
    print(f"total_cases={len(all_cases)}")
    print(f"intended_domain_cases={sum(1 for *_, intended in all_cases if intended)}")
    print(f"extension_cases={sum(1 for *_, intended in all_cases if not intended)}")
    print(f"input_set_sha256={hashlib.sha256(inputs_json.encode()).hexdigest()}")
    print(f"result_mismatches={len(result_mismatches)}")
    print(f"post_call_input_state_mismatches={post_call_input_mismatches}")
    if result_mismatches:
        print(json.dumps(result_mismatches[:10], indent=2, sort_keys=True))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
