#!/usr/bin/env python3
"""Independent CPython differential for HumanEval 28-concatenate."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import pathlib
import random
from collections.abc import Callable


def load_entry(path: pathlib.Path, module_name: str) -> Callable[[list[str]], str]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    entry = getattr(module, "concatenate")
    return entry


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8", errors="surrogatepass")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases-output", type=pathlib.Path, required=True)
    args = parser.parse_args()

    canonical = load_entry(pathlib.Path("/reference/canonical.py"), "trusted_canonical")
    generated = load_entry(
        pathlib.Path("/tmp/audit-work/fresh/solution.py"), "scratch_generated_solution"
    )

    cases: list[tuple[str, list[str]]] = [
        ("documented-empty", []),
        ("documented-abc", ["a", "b", "c"]),
        ("loop-one-empty", [""]),
        ("loop-one-nonempty", ["boundary"]),
        ("empty-elements", ["", "hello", "", " world", ""]),
        ("unicode", ["é", "β", "🙂", "e\u0301"]),
        ("controls", ["a\n", "\t", "\0", "z"]),
        ("long-list", [""] * 10_000 + ["tail"]),
        ("long-element", ["λ" * 10_000]),
    ]

    atoms = ["", "a", "β", " ", "\n"]
    for length in range(4):
        for values in itertools.product(atoms, repeat=length):
            cases.append((f"exhaustive-atoms-len-{length}", list(values)))

    rng = random.Random(28028)
    alphabet = ["", "a", "Z", "7", " ", "\n", "\t", "\0", "β", "🙂", "\u0301"]
    for number in range(256):
        value_count = rng.randrange(0, 13)
        values = [
            "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 13)))
            for _ in range(value_count)
        ]
        cases.append((f"seed-28028-generated-{number:03d}", values))

    unique_cases: list[tuple[str, list[str]]] = []
    seen: set[tuple[str, ...]] = set()
    for label, values in cases:
        key = tuple(values)
        if key not in seen:
            seen.add(key)
            unique_cases.append((label, values))

    mismatch_count = 0
    with args.cases_output.open("w", encoding="utf-8") as case_file:
        for case_id, (label, values) in enumerate(unique_cases):
            input_record = {"case_id": case_id, "label": label, "input": values}
            case_file.write(json.dumps(input_record, ensure_ascii=True) + "\n")

            expected = canonical(values)
            actual = generated(values)
            matches = (
                type(expected) is str
                and type(actual) is str
                and expected == actual
            )
            mismatch_count += int(not matches)
            result_record = {
                "case_id": case_id,
                "label": label,
                "input_items": len(values),
                "expected_length": len(expected),
                "actual_length": len(actual),
                "expected_sha256": digest(expected),
                "actual_sha256": digest(actual),
                "matches": matches,
            }
            if len(expected) <= 120 and len(actual) <= 120:
                result_record["expected"] = expected
                result_record["actual"] = actual
            print(json.dumps(result_record, ensure_ascii=True, sort_keys=True))

    corpus_hash = hashlib.sha256(args.cases_output.read_bytes()).hexdigest()
    print(
        json.dumps(
            {
                "summary": {
                    "case_count": len(unique_cases),
                    "mismatch_count": mismatch_count,
                    "case_corpus_sha256": corpus_hash,
                    "formal_input_shape": "finite list[str]",
                    "coverage": {
                        "documented_examples": 2,
                        "explicit_boundary_cases": 7,
                        "exhaustive_atom_products": "lengths 0..3 over five atoms",
                        "deterministic_generated_attempts": 256,
                        "random_seed": 28028,
                    },
                }
            },
            sort_keys=True,
        )
    )
    return 1 if mismatch_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
