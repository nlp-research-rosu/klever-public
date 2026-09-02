#!/usr/bin/env python3
"""Concrete satisfying witnesses for both positive reachability claims."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load_function(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sorted_list_sum


def scan_even(accumulator: list[str], remaining: list[str]) -> list[str]:
    return accumulator + [value for value in remaining if len(value) % 2 == 0]


def main() -> int:
    canonical = load_function(Path("/reference/canonical.py"), "ground_canonical")
    submitted = load_function(Path("/candidate/solution.py"), "ground_submitted")

    loop_input = ["aa", "b"]
    loop_accumulator = ["cc"]
    loop_post = scan_even(loop_accumulator, loop_input)
    print(
        "filter_loop_witness="
        + json.dumps(
            {
                "INPUT": loop_input,
                "ACC": loop_accumulator,
                "H": 0,
                "stringsOnly(INPUT)": all(isinstance(x, str) for x in loop_input),
                "scanEven(ACC,INPUT)": loop_post,
            },
            sort_keys=True,
        )
    )

    entry_input = ["bb", "a", "aa", "cccc"]
    canonical_arg = list(entry_input)
    submitted_arg = list(entry_input)
    canonical_result = canonical(canonical_arg)
    submitted_result = submitted(submitted_arg)
    expected = ["aa", "bb", "cccc"]
    print(
        "entry_witness="
        + json.dumps(
            {
                "INPUT": entry_input,
                "stringsOnly(INPUT)": all(isinstance(x, str) for x in entry_input),
                "claimed_scanEven": ["bb", "aa", "cccc"],
                "claimed_sortVS": ["aa", "bb", "cccc"],
                "claimed_sortKeyVS_by_len": expected,
                "trusted_canonical_result": canonical_result,
                "submitted_result": submitted_result,
                "expected": expected,
            },
            sort_keys=True,
        )
    )
    return 0 if canonical_result == submitted_result == expected else 1


if __name__ == "__main__":
    raise SystemExit(main())
