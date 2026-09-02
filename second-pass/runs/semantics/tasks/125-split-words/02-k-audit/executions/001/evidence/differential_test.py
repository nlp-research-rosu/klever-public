#!/usr/bin/env python3
"""Independent canonical-vs-generated differential test for split_words."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path
from typing import Any, Callable


def load_entry(path: Path, module_name: str) -> Callable[[str], Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.split_words


def json_value(value: Any) -> dict[str, Any]:
    return {"type": type(value).__name__, "value": value}


def main() -> int:
    if len(sys.argv) != 5:
        print(
            "usage: differential_test.py CANONICAL GENERATED INPUTS_JSON RESULTS_JSON",
            file=sys.stderr,
        )
        return 64

    canonical_path, generated_path, inputs_path, results_path = map(
        Path, sys.argv[1:]
    )
    canonical = load_entry(canonical_path, "trusted_canonical")
    generated = load_entry(generated_path, "candidate_generated")

    named_cases = [
        ("documented-space", "Hello world!"),
        ("documented-comma", "Hello,world!"),
        ("documented-count", "abcdef"),
        ("empty", ""),
        ("one-space", " "),
        ("leading-space", " a"),
        ("trailing-space", "a "),
        ("repeated-space", "a  b"),
        ("space-precedes-comma", "a,b c"),
        ("tab-only", "a\tb"),
        ("newline-only", "a\nb"),
        ("carriage-return-only", "a\rb"),
        ("vertical-tab-only", "a\vb"),
        ("form-feed-only", "a\fb"),
        ("unicode-whitespace-only", "a\u2003b"),
        ("one-comma", ","),
        ("leading-comma", ",a"),
        ("trailing-comma", "a,"),
        ("adjacent-commas", "a,,b"),
        ("two-commas", ",,"),
        ("comma-and-tab", "a,\tb"),
        ("count-a", "a"),
        ("count-b", "b"),
        ("count-z", "z"),
        ("count-uppercase", "B"),
        ("count-mixed", "abBdz!"),
        ("unicode-lower-even-codepoint", "\u00ea"),
        ("unicode-lower-odd-codepoint", "\u00e9"),
    ]

    labeled: dict[str, set[str]] = {}
    ordered_inputs: list[str] = []

    def add(value: str, label: str) -> None:
        if value not in labeled:
            labeled[value] = set()
            ordered_inputs.append(value)
        labeled[value].add(label)

    for label, value in named_cases:
        add(value, label)

    exhaustive_alphabet = ["a", "b", ",", " ", "\t", "\v"]
    for length in range(5):
        for chars in itertools.product(exhaustive_alphabet, repeat=length):
            add("".join(chars), f"exhaustive-length-{length}")

    rng = random.Random(125)
    random_alphabet = (
        list("abcdfxyzABCXYZ019!?,")
        + [" ", "\t", "\n", "\r", "\v", "\f", "\u2003", "\u00e9", "\u00ea"]
    )
    for _ in range(500):
        length = rng.randrange(0, 25)
        add(
            "".join(rng.choice(random_alphabet) for _ in range(length)),
            "deterministic-random-seed-125",
        )

    inputs_payload = {
        "oracle": str(canonical_path),
        "implementation": str(generated_path),
        "named_cases": [{"label": n, "input": s} for n, s in named_cases],
        "exhaustive_alphabet": exhaustive_alphabet,
        "exhaustive_lengths": [0, 1, 2, 3, 4],
        "random_seed": 125,
        "random_count": 500,
        "random_length_range": [0, 24],
        "random_alphabet": random_alphabet,
        "deduplicated_inputs": ordered_inputs,
        "labels_by_input": {
            value: sorted(labels) for value, labels in labeled.items()
        },
    }
    inputs_path.write_text(
        json.dumps(inputs_payload, ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )

    rows = []
    mismatch_rows = []
    for value in ordered_inputs:
        expected = canonical(value)
        actual = generated(value)
        matches = type(expected) is type(actual) and expected == actual
        row = {
            "input": value,
            "labels": sorted(labeled[value]),
            "canonical": json_value(expected),
            "generated": json_value(actual),
            "matches": matches,
        }
        rows.append(row)
        if not matches:
            mismatch_rows.append(row)

    results_payload = {
        "total": len(rows),
        "matches": len(rows) - len(mismatch_rows),
        "mismatches": len(mismatch_rows),
        "rows": rows,
    }
    results_path.write_text(
        json.dumps(results_payload, ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"TOTAL_INPUTS: {len(rows)}")
    print(f"MATCHES: {len(rows) - len(mismatch_rows)}")
    print(f"MISMATCHES: {len(mismatch_rows)}")
    for row in mismatch_rows[:50]:
        print(
            "MISMATCH:",
            repr(row["input"]),
            "labels=" + repr(row["labels"]),
            "canonical=" + repr(row["canonical"]),
            "generated=" + repr(row["generated"]),
        )
    if len(mismatch_rows) > 50:
        print(f"ADDITIONAL_MISMATCHES_IN_JSON: {len(mismatch_rows) - 50}")

    return 1 if mismatch_rows else 0


if __name__ == "__main__":
    raise SystemExit(main())
