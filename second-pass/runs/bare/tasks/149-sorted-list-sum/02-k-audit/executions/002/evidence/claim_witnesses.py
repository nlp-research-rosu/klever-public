#!/usr/bin/env python3
"""Concrete satisfying states for every entry claim in spec.k."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sorted_list_sum


def oracle(words: list[str]) -> list[str]:
    return sorted(
        (word for word in words if len(word) % 2 == 0),
        key=lambda word: (len(word), word),
    )


def main() -> int:
    canonical = load("canonical_witness", Path("/reference/canonical.py"))
    candidate = load(
        "candidate_witness", Path("/tmp/audit-work/reconstruction/solution.py")
    )
    witnesses = [
        ("universal-correctness", ["bb", "a"], True),
        ("base", [], True),
        ("symbolic-two", ["aa", "ab"], len("aa") == 2 and len("ab") == 2 and "aa" < "ab"),
        (
            "symbolic-two-reverse",
            ["ba", "ab"],
            len("ba") == 2 and len("ab") == 2 and not ("ba" < "ab"),
        ),
        (
            "symbolic-three",
            ["zzzz", "aa", "bbb"],
            len("zzzz") == 4 and len("aa") == 2 and len("bbb") == 3,
        ),
        ("prompt-example-one", ["aa", "a", "aaa"], True),
        ("prompt-example-two", ["ab", "a", "aaa", "cd"], True),
    ]
    failures = 0
    for claim, words, precondition in witnesses:
        expected = oracle(words)
        canonical_result = canonical(list(words))
        candidate_result = candidate(list(words))
        valid = precondition and canonical_result == expected == candidate_result
        failures += not valid
        print(
            json.dumps(
                {
                    "claim": claim,
                    "input": words,
                    "precondition_satisfied": precondition,
                    "formal_rhs_ground_value": expected,
                    "canonical": canonical_result,
                    "candidate": candidate_result,
                    "match": valid,
                },
                ensure_ascii=True,
                sort_keys=True,
            )
        )
    print(f"CLAIM_WITNESSES_OK={failures == 0} count={len(witnesses)}")
    return int(failures != 0)


if __name__ == "__main__":
    raise SystemExit(main())
