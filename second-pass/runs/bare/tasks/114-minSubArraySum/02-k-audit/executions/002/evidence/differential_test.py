#!/usr/bin/env python3
"""Independent candidate/canonical/brute-force differential test."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.minSubArraySum


def brute_min_subarray(values: list[int]) -> int:
    return min(
        sum(values[start:end])
        for start in range(len(values))
        for end in range(start + 1, len(values) + 1)
    )


def outcome(function, values):
    try:
        return ("return", function(list(values)))
    except Exception as error:  # Diagnostic comparison includes empty input.
        return ("raise", type(error).__name__)


def main() -> int:
    settings = json.loads(
        Path("/audit-output/evidence/differential_inputs.json").read_text(encoding="utf-8")
    )
    canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical_114")
    generated = load_entry(Path("/tmp/audit-work/source/solution.py"), "generated_solution_114")

    categorized: list[tuple[str, list[int]]] = []
    categorized += [
        ("documented", values) for values in settings["documented_examples"]
    ]
    categorized += [("curated", values) for values in settings["curated_nonempty"]]
    exhaustive = settings["exhaustive"]
    for length in exhaustive["lengths"]:
        for values in itertools.product(exhaustive["element_values"], repeat=length):
            categorized.append(("exhaustive", list(values)))
    random_settings = settings["random"]
    generator = random.Random(random_settings["seed"])
    for _ in range(random_settings["count"]):
        length = generator.randint(
            random_settings["minimum_length"], random_settings["maximum_length"]
        )
        categorized.append(
            (
                "random",
                [
                    generator.randint(
                        random_settings["minimum_element"],
                        random_settings["maximum_element"],
                    )
                    for _ in range(length)
                ],
            )
        )

    counts: dict[str, int] = {}
    mismatches: list[dict[str, object]] = []
    for category, values in categorized:
        counts[category] = counts.get(category, 0) + 1
        canonical_value = canonical(list(values))
        generated_value = generated(list(values))
        brute_value = brute_min_subarray(list(values))
        if canonical_value != generated_value or generated_value != brute_value:
            mismatches.append(
                {
                    "category": category,
                    "input": values,
                    "canonical": canonical_value,
                    "generated": generated_value,
                    "brute": brute_value,
                }
            )

    print("intended_domain_counts=" + json.dumps(counts, sort_keys=True))
    print(f"intended_domain_total={len(categorized)}")
    print(f"intended_domain_mismatches={len(mismatches)}")
    if mismatches:
        print("first_mismatches=" + json.dumps(mismatches[:20], sort_keys=True))

    for values in settings["out_of_domain"]:
        canonical_outcome = outcome(canonical, values)
        generated_outcome = outcome(generated, values)
        print(
            "out_of_domain="
            + json.dumps(
                {
                    "input": values,
                    "canonical": canonical_outcome,
                    "generated": generated_outcome,
                    "same": canonical_outcome == generated_outcome,
                },
                sort_keys=True,
            )
        )
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
