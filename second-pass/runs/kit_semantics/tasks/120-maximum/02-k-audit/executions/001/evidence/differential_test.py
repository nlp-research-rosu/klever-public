#!/usr/bin/env python3
"""Independent result differential for HumanEval 120 `maximum`."""

from __future__ import annotations

import hashlib
import heapq
import importlib.util
import json
import random
from pathlib import Path


TRUSTED = Path("/tmp/audit-work/trusted/canonical.py")
GENERATED = Path("/tmp/audit-work/candidate-source/solution.py")
INPUT_RECORD = Path("/audit-output/evidence/differential_inputs.json")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def oracle(values: list[int], k: int) -> list[int]:
    """Independent top-k construction: selection by heap, then ascending order."""
    return sorted(heapq.nlargest(k, values)) if k else []


def cases() -> list[dict[str, object]]:
    result: list[dict[str, object]] = [
        {"label": "example-1", "arr": [-3, -4, 5], "k": 3, "in_contract": True},
        {"label": "example-2", "arr": [4, -4, 4], "k": 2, "in_contract": True},
        {
            "label": "example-3",
            "arr": [-3, 2, 1, 2, -1, -2, 1],
            "k": 1,
            "in_contract": True,
        },
        {"label": "claim-witness", "arr": [1, 2], "k": 1, "in_contract": True},
        {"label": "empty-k0", "arr": [], "k": 0, "in_contract": False},
        {"label": "singleton-k0", "arr": [7], "k": 0, "in_contract": True},
        {"label": "singleton-k1", "arr": [7], "k": 1, "in_contract": True},
        {"label": "duplicates-k1", "arr": [4, 4, -4], "k": 1, "in_contract": True},
        {"label": "duplicates-k2", "arr": [4, 4, -4], "k": 2, "in_contract": True},
        {
            "label": "value-limits-k0",
            "arr": [-1000, 1000, 0, -1000, 1000],
            "k": 0,
            "in_contract": True,
        },
        {
            "label": "value-limits-klen",
            "arr": [-1000, 1000, 0, -1000, 1000],
            "k": 5,
            "in_contract": True,
        },
        {
            "label": "length-1000-k0",
            "arr": [((i * 37) % 2001) - 1000 for i in range(1000)],
            "k": 0,
            "in_contract": True,
        },
        {
            "label": "length-1000-k1",
            "arr": [((i * 37) % 2001) - 1000 for i in range(1000)],
            "k": 1,
            "in_contract": True,
        },
        {
            "label": "length-1000-k999",
            "arr": [((i * 37) % 2001) - 1000 for i in range(1000)],
            "k": 999,
            "in_contract": True,
        },
        {
            "label": "length-1000-k1000",
            "arr": [((i * 37) % 2001) - 1000 for i in range(1000)],
            "k": 1000,
            "in_contract": True,
        },
    ]
    rng = random.Random(120_2026)
    generated_index = 0
    for length in (1, 2, 3, 4, 7, 16, 50, 127):
        for _ in range(5):
            values = [rng.randint(-1000, 1000) for _ in range(length)]
            for k in sorted({0, 1, length // 2, max(0, length - 1), length}):
                result.append(
                    {
                        "label": f"generated-{generated_index:03d}",
                        "arr": values,
                        "k": k,
                        "in_contract": True,
                    }
                )
                generated_index += 1
    return result


def main() -> None:
    canonical = load(TRUSTED, "trusted_canonical")
    generated = load(GENERATED, "generated_solution")
    test_cases = cases()
    serialized = json.dumps(test_cases, sort_keys=True, separators=(",", ":"))
    INPUT_RECORD.write_text(
        json.dumps(test_cases, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"input_record={INPUT_RECORD}")
    print(f"input_count={len(test_cases)}")
    print(f"input_sha256={hashlib.sha256(serialized.encode()).hexdigest()}")
    print("random_seed=1202026")

    mismatches: list[dict[str, object]] = []
    canonical_mutations = 0
    generated_mutations = 0
    for index, case in enumerate(test_cases):
        values = list(case["arr"])
        k = int(case["k"])
        canonical_arg = values.copy()
        generated_arg = values.copy()
        canonical_value = canonical.maximum(canonical_arg, k)
        generated_value = generated.maximum(generated_arg, k)
        oracle_value = oracle(values, k)
        if canonical_arg != values:
            canonical_mutations += 1
        if generated_arg != values:
            generated_mutations += 1
        if canonical_value != generated_value or generated_value != oracle_value:
            mismatches.append(
                {
                    "index": index,
                    "case": case,
                    "canonical": canonical_value,
                    "generated": generated_value,
                    "oracle": oracle_value,
                }
            )
        if index < 14:
            shown_result: object
            if len(generated_value) > 20:
                shown_result = {
                    "length": len(generated_value),
                    "first5": generated_value[:5],
                    "last5": generated_value[-5:],
                }
            else:
                shown_result = generated_value
            print(
                f"case[{index}] label={case['label']} k={k} n={len(values)} "
                f"in_contract={case['in_contract']} result={shown_result}"
            )

    print(f"result_mismatches={len(mismatches)}")
    print(f"canonical_input_mutations={canonical_mutations}")
    print(f"generated_input_mutations={generated_mutations}")
    if mismatches:
        print(json.dumps(mismatches[:5], indent=2, sort_keys=True))
        raise SystemExit(1)
    print("DIFFERENTIAL_TEST_PASSED")


if __name__ == "__main__":
    main()
