#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and madSolution."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path("/tmp/audit-work/candidate")


def balanced_term(text: str, start: int) -> str:
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
        character = text[index]
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
                return text[start : index + 1]
    raise ValueError("unbalanced K constructor term")


def strip_space_outside_strings(text: str) -> str:
    output: list[str] = []
    in_string = False
    escaped = False
    for character in text:
        if in_string:
            output.append(character)
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
        elif character == '"':
            in_string = True
            output.append(character)
        elif not character.isspace():
            output.append(character)
    return "".join(output)


def main() -> None:
    submitted = (ROOT / "solution.mpy").read_text()
    verification = (ROOT / "verification.k").read_text()
    rule_offset = verification.index("rule madSolution =>")
    module_offset = verification.index("Module(", rule_offset)
    claimed = balanced_term(verification, module_offset)

    submitted_normalized = strip_space_outside_strings(submitted)
    claimed_normalized = strip_space_outside_strings(claimed)
    print(f"submitted_normalized_length={len(submitted_normalized)}")
    print(f"claim_normalized_length={len(claimed_normalized)}")
    print(
        "submitted_normalized_sha256="
        + hashlib.sha256(submitted_normalized.encode()).hexdigest()
    )
    print(
        "claim_normalized_sha256="
        + hashlib.sha256(claimed_normalized.encode()).hexdigest()
    )
    print(f"constructor_terms_identical={submitted_normalized == claimed_normalized}")
    assert submitted_normalized == claimed_normalized

    run_rule = (
        '#runMad(V:Val) => #loadAll(madSolution)\n'
        '                              ~> Call(Name("mean_absolute_deviation"), V)'
    )
    assert run_rule in verification
    print("entry_rule_loads_madSolution_then_calls_bound_entry=true")


if __name__ == "__main__":
    main()
