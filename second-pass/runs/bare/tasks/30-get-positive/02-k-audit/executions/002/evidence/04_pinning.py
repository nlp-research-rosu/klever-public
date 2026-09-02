#!/usr/bin/env python3
"""Mechanically compare translated and claimed constructor terms."""

from __future__ import annotations

import re
from pathlib import Path


def balanced_module_terms(text: str) -> list[str]:
    terms: list[str] = []
    cursor = 0
    while True:
        start = text.find("Module(", cursor)
        if start < 0:
            return terms
        depth = 0
        in_string = False
        escaped = False
        for end in range(start, len(text)):
            character = text[end]
            if in_string:
                if escaped:
                    escaped = False
                elif character == "\\":
                    escaped = True
                elif character == '"':
                    in_string = False
                continue
            if character == '"':
                in_string = True
            elif character == "(":
                depth += 1
            elif character == ")":
                depth -= 1
                if depth == 0:
                    terms.append(text[start : end + 1])
                    cursor = end + 1
                    break
        else:
            raise ValueError(f"unbalanced Module term at offset {start}")


def normalize(term: str) -> str:
    return re.sub(r"\s+", "", term)


def main() -> int:
    root = Path("/tmp/audit-work/30-get-positive/candidate-src")
    regenerated = normalize((root / "solution.trusted-regenerated.mpy").read_text())
    submitted = normalize((root / "solution.mpy").read_text())
    print(f"TRANSLATION submitted_equals_trusted={submitted == regenerated}")
    all_equal = submitted == regenerated
    for file_name, expected_count in [
        ("verification.k", 3),
        ("spec.k", 5),
    ]:
        terms = balanced_module_terms((root / file_name).read_text())
        print(f"CLAIM_TERMS file={file_name} count={len(terms)}")
        if len(terms) != expected_count:
            all_equal = False
        for index, term in enumerate(terms, 1):
            equal = normalize(term) == regenerated
            all_equal = all_equal and equal
            print(
                f"CLAIM_TERM file={file_name} index={index} "
                f"equals_trusted_translation={equal}"
            )

    mutated_translation = root / "solution-threshold-one.mpy"
    mutated_spec = root / "spec-body-sensitivity.k"
    if mutated_translation.exists() and mutated_spec.exists():
        mutated_terms = balanced_module_terms(mutated_spec.read_text())
        mutated_equal = (
            len(mutated_terms) == 1
            and normalize(mutated_terms[0])
            == normalize(mutated_translation.read_text())
        )
        all_equal = all_equal and mutated_equal
        print(
            "BODY_MUTATION "
            f"claim_term_equals_trusted_mutated_translation={mutated_equal}"
        )

    witnesses = [
        ("universal", [-1, 0, 2], [2]),
        ("helper_positive_head", [3, -2, 4], [3, 4]),
        ("helper_nonpositive_head", [0, -2, 4], [4]),
        ("helper_empty", [], []),
        ("example_one", [-1, 2, -4, 5, 6], [2, 5, 6]),
        (
            "example_two",
            [5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10],
            [5, 3, 2, 3, 9, 123, 1],
        ),
        ("spec_empty", [], []),
        ("all_nonpositive", [0, -1, -2], []),
    ]
    for label, values, claimed in witnesses:
        actual = [value for value in values if value > 0]
        ok = actual == claimed
        all_equal = all_equal and ok
        print(
            f"WITNESS claim={label} precondition_satisfied=True "
            f"input={values!r} claimed={claimed!r} "
            f"python_canonical_and_candidate={actual!r} equal={ok}"
        )
    return 0 if all_equal else 1


if __name__ == "__main__":
    raise SystemExit(main())
