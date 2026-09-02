#!/usr/bin/env python3
"""Independent docstring/canonical differential for HumanEval 153."""

from __future__ import annotations

import importlib.util
import random
import string
import sys
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Strongest_Extension


def score_cpython(text: str) -> int:
    return sum(ch.isupper() for ch in text) - sum(ch.islower() for ch in text)


def score_fixed_ascii_model(text: str) -> int:
    return sum("A" <= ch <= "Z" for ch in text) - sum(
        "a" <= ch <= "z" for ch in text
    )


def first_max_result(class_name: str, extensions: list[str]) -> str:
    if not extensions:
        return class_name + "."
    scores = [score_cpython(extension) for extension in extensions]
    winner_index = max(range(len(extensions)), key=scores.__getitem__)
    return class_name + "." + extensions[winner_index]


def fixed_model_result(class_name: str, extensions: list[str]) -> str:
    if not extensions:
        return class_name + "."
    scores = [score_fixed_ascii_model(extension) for extension in extensions]
    winner_index = max(range(len(extensions)), key=scores.__getitem__)
    return class_name + "." + extensions[winner_index]


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: independent_differential.py SOLUTION CANONICAL", file=sys.stderr)
        return 64

    generated = load_entry(Path(sys.argv[1]), "audited_solution")
    canonical = load_entry(Path(sys.argv[2]), "trusted_canonical")

    directed = [
        ("doc_slices", "Slices", ["SErviNGSliCes", "Cheese", "StuFfed"]),
        ("doc_tie", "my_class", ["AA", "Be", "CC"]),
        ("initial_none", "C", ["abc"]),
        ("uppercase_branch", "C", ["", "Z"]),
        ("lowercase_branch", "C", ["", "z"]),
        ("neither_branch", "C", ["9-_", ""]),
        ("strict_greater", "C", ["a", "A"]),
        ("equal_tie_first", "C", ["Ab", "Cd", "XYzz"]),
        ("less_no_update", "C", ["AA", "bbb"]),
        ("empty_extension", "", [""]),
        ("unicode_upper", "Κλάση", ["", "Ω"]),
        ("unicode_lower", "Κλάση", ["", "ω"]),
        ("titlecase", "C", ["", "ǅ"]),
        ("uncased_unicode", "C", ["", "中"]),
        ("combining", "C", ["A\u0301", "a\u0301"]),
    ]

    failures: list[str] = []
    compared_with_canonical = 0
    for label, class_name, extensions in directed:
        expected = first_max_result(class_name, extensions)
        got = generated(class_name, list(extensions))
        reference = canonical(class_name, list(extensions))
        compared_with_canonical += 1
        print(
            "DIRECTED",
            label,
            repr((class_name, extensions)),
            "generated=",
            repr(got),
            "canonical=",
            repr(reference),
            "doc_oracle=",
            repr(expected),
        )
        if got != expected:
            failures.append(f"{label}: generated {got!r} != doc oracle {expected!r}")
        if reference != expected:
            failures.append(f"{label}: canonical {reference!r} != doc oracle {expected!r}")

    empty_class = "Empty"
    empty_generated = generated(empty_class, [])
    try:
        empty_canonical = canonical(empty_class, [])
        empty_canonical_outcome = f"returned {empty_canonical!r}"
    except Exception as err:  # The canonical witness indexes extensions[0].
        empty_canonical_outcome = f"raised {type(err).__name__}: {err}"
    print(
        "UNDERDETERMINED_EMPTY_LIST",
        "generated=",
        repr(empty_generated),
        "canonical=",
        empty_canonical_outcome,
    )
    if empty_generated != "Empty.":
        failures.append("candidate empty-list policy changed unexpectedly")

    rng = random.Random(153_20260730)
    alphabet = string.ascii_letters + string.digits + "._- Ωωǅ中éÉß"
    random_cases = 10_000
    canonical_mismatches = 0
    oracle_mismatches = 0
    for case_index in range(random_cases):
        class_name = "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 9)))
        extensions = [
            "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 13)))
            for _ in range(rng.randrange(1, 9))
        ]
        got = generated(class_name, list(extensions))
        reference = canonical(class_name, list(extensions))
        expected = first_max_result(class_name, extensions)
        compared_with_canonical += 1
        if got != reference:
            canonical_mismatches += 1
            if canonical_mismatches <= 5:
                print(
                    "CANONICAL_MISMATCH",
                    case_index,
                    repr((class_name, extensions, got, reference)),
                )
        if got != expected:
            oracle_mismatches += 1
            if oracle_mismatches <= 5:
                print(
                    "ORACLE_MISMATCH",
                    case_index,
                    repr((class_name, extensions, got, expected)),
                )

    gap_input = ("Gap", ["", "Ω"])
    python_gap = generated(gap_input[0], list(gap_input[1]))
    model_gap = fixed_model_result(gap_input[0], list(gap_input[1]))
    print(
        "SUPPLIED_MODEL_DIVERGENCE_WITNESS",
        repr(gap_input),
        "cpython=",
        repr(python_gap),
        "fixed_ascii_model=",
        repr(model_gap),
    )
    if python_gap == model_gap:
        failures.append("chosen model-divergence witness did not diverge")

    print(
        "SUMMARY",
        f"directed_nonempty={len(directed)}",
        f"random_nonempty={random_cases}",
        f"canonical_compared={compared_with_canonical}",
        f"canonical_mismatches={canonical_mismatches}",
        f"doc_oracle_mismatches={oracle_mismatches}",
        f"failures={len(failures)}",
    )
    for failure in failures:
        print("FAILURE", failure)
    return 1 if failures or canonical_mismatches or oracle_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
