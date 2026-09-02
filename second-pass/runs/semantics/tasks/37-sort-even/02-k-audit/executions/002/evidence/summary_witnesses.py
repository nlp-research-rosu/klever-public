#!/usr/bin/env python3
"""Ground witnesses for the entry claim's mathematical result summary."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path("/tmp/audit-work/37-sort-even")


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_even


def claimed_summary(values: list[int]) -> dict[str, object]:
    even_indices = values[::2]
    odd_indices = values[1::2]
    # This line is the explicit interpretation of the supplied opaque primitive:
    # sortVS(even_indices) is assumed to mean Python's ascending sorted().
    sorted_evens = sorted(even_indices)
    paired: list[int] = []
    for index, odd in enumerate(odd_indices):
        paired.extend([sorted_evens[index], odd])
    suffix = sorted_evens[len(odd_indices) :]
    result = paired + suffix
    return {
        "evenIndices": even_indices,
        "oddIndices": odd_indices,
        "sortVS_interpreted_as_sorted": sorted_evens,
        "pairedVS": paired,
        "evenSuffix": suffix,
        "assembledEvenSort": result,
    }


def main() -> int:
    canonical = load_function(ROOT / "canonical.py", "witness_canonical_37")
    generated = load_function(ROOT / "solution.py", "witness_generated_37")
    inputs = [
        [],
        [7],
        [5, 6, 3, 4],
        [9, -1, 3, -2, 3, -3, 0],
    ]
    failures = 0
    for values in inputs:
        summary = claimed_summary(values)
        canon = canonical(list(values))
        generated_result = generated(list(values))
        agrees = summary["assembledEvenSort"] == canon == generated_result
        failures += not agrees
        print(
            json.dumps(
                {
                    "input": values,
                    "formal_summary_components": summary,
                    "trusted_canonical": canon,
                    "generated_python": generated_result,
                    "all_equal": agrees,
                },
                sort_keys=True,
            )
        )
    print(f"WITNESS_COUNT={len(inputs)}")
    print(f"FAILURE_COUNT={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
