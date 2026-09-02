#!/usr/bin/env python3
"""Independent candidate/canonical differential test for problem 127."""

import argparse
import importlib.util
import json
import random
from pathlib import Path


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def generated_cases():
    rng = random.Random(127)
    for _ in range(4000):
        base = rng.randint(-10**12, 10**12)
        a = base + rng.randint(-50, 50)
        b = a + rng.randint(0, 50)
        c = base + rng.randint(-50, 50)
        d = c + rng.randint(0, 50)
        yield (a, b), (c, d)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_manifest", type=Path)
    args = parser.parse_args()

    canonical = load_module("trusted_canonical", "/reference/canonical.py")
    candidate = load_module(
        "scratch_generated_solution", "/tmp/audit-work/scratch/solution.py"
    )

    explicit = [
        ("prompt-1", (1, 2), (2, 3), "NO"),
        ("prompt-2", (-1, 1), (0, 4), "NO"),
        ("prompt-3", (-3, -1), (-5, 5), "YES"),
        ("singleton-identical", (0, 0), (0, 0), "NO"),
        ("touching", (0, 2), (2, 5), "NO"),
        ("disjoint-left", (-5, -4), (2, 3), "NO"),
        ("disjoint-right", (2, 3), (-5, -4), "NO"),
        ("length-one", (0, 1), (0, 1), "NO"),
        ("length-two", (0, 2), (0, 2), "YES"),
        ("length-three", (0, 3), (0, 3), "YES"),
        ("length-four", (0, 4), (0, 4), "NO"),
        ("left-branch-greater", (0, 10), (3, 10), "YES"),
        ("left-branch-equal", (3, 10), (3, 8), "YES"),
        ("left-branch-less", (3, 10), (0, 10), "YES"),
        ("right-branch-less", (0, 10), (0, 3), "YES"),
        ("right-branch-equal", (0, 3), (0, 3), "YES"),
        ("right-branch-greater", (0, 3), (0, 10), "YES"),
        ("nested-prime", (-100, 100), (-2, 3), "YES"),
        ("nested-composite", (-100, 100), (-2, 4), "NO"),
    ]

    cases = []
    for label, first, second, expected in explicit:
        cases.append(("explicit:" + label, first, second, expected))

    intervals = [
        (start, end)
        for start in range(-8, 9)
        for end in range(start, 9)
    ]
    for first in intervals:
        for second in intervals:
            cases.append(("exhaustive[-8,8]", first, second, None))

    for first, second in generated_cases():
        cases.append(("generated-seed-127", first, second, None))

    mismatches = []
    explicit_failures = []
    source_counts = {}
    with args.input_manifest.open("w", encoding="utf-8") as manifest:
        for source, first, second, expected in cases:
            trusted_result = canonical.intersection(first, second)
            candidate_result = candidate.intersection(first, second)
            source_counts[source.split(":", 1)[0]] = (
                source_counts.get(source.split(":", 1)[0], 0) + 1
            )
            record = {
                "source": source,
                "interval1": first,
                "interval2": second,
                "canonical": trusted_result,
                "candidate": candidate_result,
            }
            manifest.write(json.dumps(record, separators=(",", ":")) + "\n")
            if trusted_result != candidate_result:
                mismatches.append(record)
            if expected is not None and (
                trusted_result != expected or candidate_result != expected
            ):
                explicit_failures.append(
                    {**record, "expected": expected}
                )

    print(
        "cases="
        f"{len(cases)} explicit={source_counts['explicit']} "
        f"exhaustive={source_counts['exhaustive[-8,8]']} "
        f"generated={source_counts['generated-seed-127']} "
        f"mismatches={len(mismatches)} "
        f"explicit_failures={len(explicit_failures)}"
    )
    print(f"input_manifest={args.input_manifest}")
    if mismatches:
        print("first_mismatches=" + json.dumps(mismatches[:10]))
    if explicit_failures:
        print("explicit_failures=" + json.dumps(explicit_failures))
    if mismatches or explicit_failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
