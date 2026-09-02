#!/usr/bin/env python3
"""Independent canonical-versus-generated differential test.

The trusted canonical module and the scratch-copied generated module are loaded
under distinct names.  The fixed seed and complete input list are emitted before
the per-case outcomes.
"""

from __future__ import annotations

import importlib.util
import json
import multiprocessing
import random
import sys
from collections.abc import Callable
from typing import Any


CANONICAL_PATH = "/tmp/audit-work/123-get-odd-collatz/trusted/canonical.py"
GENERATED_PATH = "/tmp/audit-work/123-get-odd-collatz/candidate-src/solution.py"


def load(path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def outcome(function: Callable[[Any], Any], value: Any) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": function(value)}
    except Exception as error:  # The exception type/message are evidence.
        return {
            "kind": "exception",
            "type": type(error).__name__,
            "message": str(error),
        }


def child_outcome(path: str, module_name: str, value: Any, queue) -> None:
    module = load(path, module_name)
    queue.put(outcome(module.get_odd_collatz, value))


def timed_outcome(path: str, module_name: str, value: Any) -> dict[str, Any]:
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(
        target=child_outcome, args=(path, module_name, value, queue)
    )
    process.start()
    process.join(0.25)
    if process.is_alive():
        process.terminate()
        process.join()
        return {"kind": "timeout", "seconds": 0.25}
    if queue.empty():
        return {"kind": "child-exit", "exitcode": process.exitcode}
    return queue.get()


def comparable(left: dict[str, Any], right: dict[str, Any]) -> bool:
    if left["kind"] != right["kind"]:
        return False
    if left["kind"] == "return":
        return left["value"] == right["value"]
    if left["kind"] == "exception":
        return left["type"] == right["type"]
    return left == right


def main() -> int:
    canonical = load(CANONICAL_PATH, "trusted_canonical")
    generated = load(GENERATED_PATH, "audited_generated")

    rng = random.Random(123)
    random_inputs = rng.sample(range(1, 5001), 64)
    cases: list[tuple[str, Any]] = [
        ("documented-example", 5),
        ("empty-out-of-domain", []),
        ("zero-out-of-domain-nontermination", 0),
        ("positive-boundary", 1),
        ("first-even-branch", 2),
        ("first-odd-loop-branch", 3),
        ("even-to-even-boundary", 4),
        ("mixed-branch-example", 6),
        ("longer-branch-example", 7),
        ("power-of-two", 16),
        ("long-trace", 27),
    ]
    cases.extend(("seed-123-generated", value) for value in random_inputs)
    cases.extend(
        [
            ("float-exactness-control", 2**53),
            ("float-rounding-boundary", 2 * (2**53 + 1)),
            ("larger-float-rounding-boundary", 2**60 + 2),
        ]
    )

    print(
        json.dumps(
            {
                "oracle": CANONICAL_PATH,
                "generated": GENERATED_PATH,
                "random_seed": 123,
                "random_inputs": random_inputs,
                "cases": [{"category": category, "input": value} for category, value in cases],
            },
            sort_keys=True,
        )
    )

    mismatches = 0
    in_domain_mismatches = 0
    for index, (category, value) in enumerate(cases):
        if category == "zero-out-of-domain-nontermination":
            canonical_result = timed_outcome(
                CANONICAL_PATH, f"canonical_child_{index}", value
            )
            generated_result = timed_outcome(
                GENERATED_PATH, f"generated_child_{index}", value
            )
        else:
            canonical_result = outcome(canonical.get_odd_collatz, value)
            generated_result = outcome(generated.get_odd_collatz, value)
        same = comparable(canonical_result, generated_result)
        if not same:
            mismatches += 1
            if category != "empty-out-of-domain" and not category.startswith("zero-"):
                in_domain_mismatches += 1
        print(
            json.dumps(
                {
                    "index": index,
                    "category": category,
                    "input": value,
                    "canonical": canonical_result,
                    "generated": generated_result,
                    "same": same,
                },
                sort_keys=True,
            )
        )

    print(
        json.dumps(
            {
                "summary": {
                    "case_count": len(cases),
                    "mismatches": mismatches,
                    "in_domain_mismatches": in_domain_mismatches,
                }
            },
            sort_keys=True,
        )
    )
    return 1 if in_domain_mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
