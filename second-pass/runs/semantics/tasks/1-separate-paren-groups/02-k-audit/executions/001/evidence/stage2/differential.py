#!/usr/bin/env python3
"""Independent intended-domain differential test for HumanEval problem 1."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path
from types import ModuleType


TRUSTED = Path("/reference/canonical.py")
GENERATED = Path("/candidate/solution.py")
INPUT_RECORD = Path("/audit-output/evidence/stage2/differential-inputs.jsonl")


def load(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def dyck_words(pairs: int) -> list[str]:
    values: list[str] = []

    def visit(prefix: str, opens: int, closes: int) -> None:
        if opens == pairs and closes == pairs:
            values.append(prefix)
            return
        if opens < pairs:
            visit(prefix + "(", opens + 1, closes)
        if closes < opens:
            visit(prefix + ")", opens, closes + 1)

    visit("", 0, 0)
    return values


def add_gap_spaces(value: str, mask: int) -> str:
    pieces: list[str] = []
    for gap in range(len(value) + 1):
        if mask & (1 << gap):
            pieces.append(" ")
        if gap < len(value):
            pieces.append(value[gap])
    return "".join(pieces)


def random_balanced(rng: random.Random, max_groups: int = 8, max_depth: int = 8) -> str:
    groups: list[str] = []
    for _ in range(rng.randint(0, max_groups)):
        remaining = rng.randint(1, max_depth)
        depth = 0
        group: list[str] = []
        while remaining or depth:
            if remaining and (depth == 0 or rng.randrange(2) == 0):
                group.append("(")
                depth += 1
                remaining -= 1
            else:
                group.append(")")
                depth -= 1
            if rng.randrange(4) == 0:
                group.append(" " * rng.randint(1, 3))
        groups.append("".join(group))
        if rng.randrange(3) != 0:
            groups.append(" " * rng.randint(1, 3))
    return "".join(groups)


def intended_oracle(value: str) -> list[str]:
    """Grammar-based oracle, independent of both Python implementations."""
    groups: list[str] = []
    current: list[str] = []
    depth = 0
    for character in value:
        if character == " ":
            continue
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
        else:
            raise ValueError("outside intended alphabet")
        current.append(character)
        if depth == 0:
            groups.append("".join(current))
            current.clear()
        if depth < 0:
            raise ValueError("unbalanced prefix")
    if depth != 0:
        raise ValueError("unbalanced suffix")
    return groups


def main() -> int:
    canonical = load(TRUSTED, "trusted_canonical")
    generated = load(GENERATED, "generated_solution")

    cases: set[str] = {
        "",
        " ",
        "   ",
        "()",
        "( )",
        "(())",
        "()()",
        " () ",
        "  (()())() ",
        "( ) (( )) (( )( ))",
        "(((())))",
        "() (()) (()()) ((()))",
        "(((((((((())))))))))",
    }
    for pairs in range(5):
        for word in dyck_words(pairs):
            for mask in range(1 << (len(word) + 1)):
                cases.add(add_gap_spaces(word, mask))

    rng = random.Random(20260724)
    for _ in range(1000):
        cases.add(random_balanced(rng))

    mismatches: list[dict[str, object]] = []
    ordered = sorted(cases, key=lambda item: (len(item), item))
    with INPUT_RECORD.open("w", encoding="utf-8") as stream:
        for value in ordered:
            expected = intended_oracle(value)
            trusted_result = canonical.separate_paren_groups(value)
            generated_result = generated.separate_paren_groups(value)
            record = {
                "input": value,
                "oracle": expected,
                "trusted": trusted_result,
                "generated": generated_result,
            }
            stream.write(json.dumps(record, ensure_ascii=True, sort_keys=True) + "\n")
            if trusted_result != expected or generated_result != expected:
                mismatches.append(record)

    outside_domain = ["\t()", "a()", "(x)", "(\n)"]
    outside_results = [
        {
            "input": value,
            "trusted": canonical.separate_paren_groups(value),
            "generated": generated.separate_paren_groups(value),
        }
        for value in outside_domain
    ]
    input_hash = hashlib.sha256(INPUT_RECORD.read_bytes()).hexdigest()
    print(f"intended_domain_case_count={len(ordered)}")
    print(f"input_record_sha256={input_hash}")
    print(f"mismatch_count={len(mismatches)}")
    if mismatches:
        for mismatch in mismatches[:20]:
            print("MISMATCH", json.dumps(mismatch, sort_keys=True))
    print("outside_domain_probes=" + json.dumps(outside_results, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
