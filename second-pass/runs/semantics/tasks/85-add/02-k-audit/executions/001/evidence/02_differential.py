#!/usr/bin/env python3
"""Differentially compare trusted canonical.add and scratch candidate add."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--preserve-cases", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_module("trusted_canonical", args.canonical)
    candidate = load_module("scratch_candidate", args.candidate)
    documented = json.loads(args.inputs.read_text(encoding="utf-8"))

    cases: list[dict[str, object]] = list(documented)
    domain = [-3, -2, -1, 0, 1, 2, 3]
    for length in range(0, 6):
        for values in itertools.product(domain, repeat=length):
            cases.append({"name": f"exhaustive_small_len_{length}", "input": list(values)})

    seed = 850085
    rng = random.Random(seed)
    for index in range(1000):
        length = rng.randint(1, 40)
        values = [rng.randint(-(10**30), 10**30) for _ in range(length)]
        cases.append({"name": f"generated_seed_{seed}_{index}", "input": values})

    encoded = json.dumps(cases, separators=(",", ":"), sort_keys=True)
    args.preserve_cases.write_text(encoded + "\n", encoding="utf-8")
    digest = hashlib.sha256(encoded.encode("utf-8")).hexdigest()

    mismatches: list[dict[str, object]] = []
    sample_results = []
    for index, case in enumerate(cases):
        values = case["input"]
        expected = canonical.add(list(values))
        actual = candidate.add(list(values))
        if index < len(documented):
            sample_results.append(
                {
                    "name": case["name"],
                    "input": values,
                    "canonical": expected,
                    "candidate": actual,
                }
            )
        if actual != expected:
            mismatches.append(
                {
                    "index": index,
                    "name": case["name"],
                    "input": values,
                    "canonical": expected,
                    "candidate": actual,
                }
            )

    print(f"documented_and_boundary_cases={len(documented)}")
    print(f"exhaustive_small_domain={domain} lengths=0..5 count={sum(len(domain) ** n for n in range(6))}")
    print(f"generated_seed={seed} generated_count=1000 lengths=1..40 values=[-10^30,10^30]")
    print(f"total_cases={len(cases)}")
    print(f"preserved_cases_sha256={digest}")
    print("documented_and_boundary_results=" + json.dumps(sample_results, sort_keys=True))
    print(f"mismatch_count={len(mismatches)}")
    if mismatches:
        print("first_mismatches=" + json.dumps(mismatches[:20], sort_keys=True))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
