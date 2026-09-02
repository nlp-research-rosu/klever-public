#!/usr/bin/env python3
"""Independent differential test for trusted canonical.py and submitted solution.py."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import pathlib
import random
import sys
from typing import Callable


def load_entry(module_name: str, path: pathlib.Path) -> Callable[[str], list[str]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    entry = getattr(module, "all_prefixes")
    return entry


def build_cases(config: dict[str, object]) -> list[str]:
    cases = list(config["documented_examples"]) + list(
        config["boundary_and_edge_cases"]
    )

    exhaustive_alphabet = list(config["exhaustive_alphabet"])
    for length in range(int(config["exhaustive_max_length"]) + 1):
        cases.extend(
            "".join(chars)
            for chars in itertools.product(exhaustive_alphabet, repeat=length)
        )

    rng = random.Random(int(config["random_seed"]))
    random_alphabet = list(config["random_alphabet"])
    for _ in range(int(config["random_count"])):
        length = rng.randrange(int(config["random_max_length"]) + 1)
        cases.append("".join(rng.choice(random_alphabet) for _ in range(length)))

    # Stable de-duplication keeps the first occurrence and therefore preserves
    # the explicitly listed boundary cases before generated cases.
    return list(dict.fromkeys(cases))


def main() -> int:
    if len(sys.argv) != 4:
        print(
            f"usage: {sys.argv[0]} CONFIG TRUSTED_CANONICAL SUBMITTED_SOLUTION",
            file=sys.stderr,
        )
        return 64

    config_path = pathlib.Path(sys.argv[1])
    canonical_path = pathlib.Path(sys.argv[2])
    solution_path = pathlib.Path(sys.argv[3])
    config = json.loads(config_path.read_text(encoding="utf-8"))
    cases = build_cases(config)

    canonical = load_entry("trusted_canonical", canonical_path)
    generated = load_entry("submitted_solution", solution_path)

    mismatches: list[dict[str, object]] = []
    for case in cases:
        expected = canonical(case)
        actual = generated(case)
        direct_contract = [case[: index + 1] for index in range(len(case))]
        if expected != actual or expected != direct_contract:
            mismatches.append(
                {
                    "input": case,
                    "canonical": expected,
                    "submitted": actual,
                    "direct_contract": direct_contract,
                }
            )

    serialized = json.dumps(
        cases, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    print(f"CONFIG: {config_path}")
    print(f"TRUSTED_ORACLE: {canonical_path}:all_prefixes")
    print(f"SUBMITTED_ENTRY: {solution_path}:all_prefixes")
    print("INTENDED_DOMAIN: Python str values")
    print(f"EXECUTED_INPUT_COUNT: {len(cases)}")
    print(f"EXECUTED_INPUTS_SHA256: {hashlib.sha256(serialized).hexdigest()}")
    print(
        "EXECUTED_INPUTS_JSON: "
        + json.dumps(cases, ensure_ascii=True, separators=(",", ":"))
    )
    print(f"MISMATCH_COUNT: {len(mismatches)}")
    if mismatches:
        print("MISMATCHES: " + json.dumps(mismatches, ensure_ascii=True))
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
