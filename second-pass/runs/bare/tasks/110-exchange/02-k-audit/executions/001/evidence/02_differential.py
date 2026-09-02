#!/usr/bin/env python3
"""Independent differential test for HumanEval 110-exchange.

Oracle: /reference/canonical.py
Candidate Python entry point: /tmp/audit-work/110-exchange/solution.py

The JSONL output is a complete record of all generated inputs and both results.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path
from typing import Any, Callable


ORACLE_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/110-exchange/solution.py")


def load_exchange(path: Path, module_name: str) -> Callable[[list[Any], list[Any]], str]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.exchange


def outcome(function: Callable[..., Any], left: list[Any], right: list[Any]) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": function(list(left), list(right))}
    except Exception as error:  # Preserve differential exception behavior.
        return {"kind": "exception", "type": type(error).__name__, "message": str(error)}


def integer_lists(values: tuple[int, ...], maximum_length: int) -> list[list[int]]:
    return [
        list(items)
        for length in range(maximum_length + 1)
        for items in itertools.product(values, repeat=length)
    ]


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} OUTPUT.jsonl", file=sys.stderr)
        return 64

    output_path = Path(sys.argv[1])
    oracle = load_exchange(ORACLE_PATH, "trusted_exchange_oracle")
    candidate = load_exchange(CANDIDATE_PATH, "audited_exchange_candidate")

    cases: list[tuple[str, list[Any], list[Any], str]] = [
        ("intended_nonempty_integer", [1, 2, 3, 4], [1, 2, 3, 4], "prompt-example-yes"),
        ("intended_nonempty_integer", [1, 2, 3, 4], [1, 5, 3, 4], "prompt-example-no"),
        ("boundary_empty_integer", [], [], "both-empty"),
        ("boundary_empty_integer", [], [1], "empty-left"),
        ("boundary_empty_integer", [2], [], "empty-right-all-even"),
        ("boundary_empty_integer", [1], [], "empty-right-odd"),
        ("intended_nonempty_integer", [1, 1], [1], "branch-gap-minus-two"),
        ("intended_nonempty_integer", [1, 1], [2], "branch-gap-minus-one"),
        ("intended_nonempty_integer", [1, 1], [2, 4], "branch-gap-zero"),
        ("intended_nonempty_integer", [2, 2], [2], "branch-gap-plus-one"),
        ("intended_nonempty_integer", [-4, -3, -2, -1], [-8, -7], "negative-parity"),
        ("intended_nonempty_integer", [0], [1], "zero-is-even"),
        ("extended_nonintegral", [0.5], [1.0], "nonintegral-number"),
        ("extended_nonintegral", [2.0, 0.25], [3.0], "mixed-integral-float"),
    ]

    exhaustive = integer_lists((-3, -2, -1, 0, 1, 2, 3), 2)
    for left in exhaustive:
        for right in exhaustive:
            domain = (
                "intended_nonempty_integer"
                if left and right
                else "boundary_empty_integer"
            )
            cases.append((domain, left, right, "exhaustive-length-0-to-2"))

    generator = random.Random(110)
    for _ in range(5000):
        left = [generator.randint(-1000, 1000) for _ in range(generator.randint(1, 12))]
        right = [generator.randint(-1000, 1000) for _ in range(generator.randint(1, 12))]
        cases.append(("intended_nonempty_integer", left, right, "seeded-random"))

    mismatch_counts: dict[str, int] = {}
    case_counts: dict[str, int] = {}
    branch_gaps: set[int] = set()
    digest = hashlib.sha256()

    with output_path.open("w", encoding="utf-8") as stream:
        for index, (domain, left, right, source) in enumerate(cases):
            expected = outcome(oracle, left, right)
            actual = outcome(candidate, left, right)
            match = expected == actual
            record = {
                "index": index,
                "domain": domain,
                "source": source,
                "lst1": left,
                "lst2": right,
                "oracle": expected,
                "candidate": actual,
                "match": match,
            }
            encoded = json.dumps(record, sort_keys=True, separators=(",", ":"))
            stream.write(encoded + "\n")
            digest.update((encoded + "\n").encode())
            case_counts[domain] = case_counts.get(domain, 0) + 1
            if not match:
                mismatch_counts[domain] = mismatch_counts.get(domain, 0) + 1
            if domain.endswith("integer"):
                total_even = sum(value % 2 == 0 for value in left + right)
                gap = total_even - len(left)
                branch_gaps.add(-1 if gap < 0 else (1 if gap > 0 else 0))

    print(f"oracle={ORACLE_PATH}")
    print(f"candidate={CANDIDATE_PATH}")
    print(f"output={output_path}")
    print(f"records={len(cases)}")
    print(f"case_counts={json.dumps(case_counts, sort_keys=True)}")
    print(f"mismatch_counts={json.dumps(mismatch_counts, sort_keys=True)}")
    print(f"branch_gap_signs={sorted(branch_gaps)}")
    print(f"jsonl_sha256={digest.hexdigest()}")

    intended_mismatches = mismatch_counts.get("intended_nonempty_integer", 0)
    empty_mismatches = mismatch_counts.get("boundary_empty_integer", 0)
    if intended_mismatches or empty_mismatches:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
