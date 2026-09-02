#!/usr/bin/env python3
"""Independent canonical-versus-candidate differential test for HumanEval 125."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.split_words


def escaped(text: str) -> str:
    return text.encode("unicode_escape").decode("ascii")


def main() -> None:
    print("COMMAND: python3 /audit-output/evidence/differential_test.py")
    canonical = load_entry(
        Path("/tmp/audit-work/trusted/canonical.py"), "trusted_canonical"
    )
    candidate = load_entry(
        Path("/tmp/audit-work/candidate/solution.py"), "generated_solution"
    )

    documented_and_boundaries = [
        "Hello world!",
        "Hello,world!",
        "abcdef",
        "",
        " ",
        ",",
        "a b",
        "a,b",
        "a,,b,",
        ",a",
        "a,",
        "a,b c",
        "a,\tb",
        "left\tright",
        "left\u2003right",
        "bdfhjlnprtvxz",
        "acegikmoqsuwy",
        "ê",  # lowercase Unicode with even code point U+00EA
        "é",  # lowercase Unicode with odd code point U+00E9
    ]

    alphabet = ("a", "b", ",", " ", "\t", "\u2003", "ê", "A")
    exhaustive = [
        "".join(chars)
        for length in range(5)
        for chars in itertools.product(alphabet, repeat=length)
    ]

    rng = random.Random(125)
    random_alphabet = (
        "abcdfxzXYZ, \t\n\u2003\u00a0éêß\u03b1\u03b2\u4e2d!09"
    )
    generated = [
        "".join(rng.choice(random_alphabet) for _ in range(rng.randrange(0, 21)))
        for _ in range(2000)
    ]

    ordered: list[str] = []
    seen: set[str] = set()
    for value in documented_and_boundaries + exhaustive + generated:
        if value not in seen:
            ordered.append(value)
            seen.add(value)

    mismatches: list[tuple[str, object, object]] = []
    for text in ordered:
        expected = canonical(text)
        actual = candidate(text)
        if actual != expected:
            mismatches.append((text, expected, actual))

    print(
        "SCOPE: documented examples + 19 explicit empty/branch/boundary cases; "
        "all strings of length 0..4 over 8 symbols; 2000 seeded strings of "
        "length 0..20 over 26 ASCII/Unicode symbols"
    )
    print(f"UNIQUE_INPUTS: {len(ordered)}")
    print(f"MISMATCHES: {len(mismatches)}")
    for text, expected, actual in mismatches[:40]:
        print(
            f"MISMATCH input={escaped(text)!r} "
            f"canonical={expected!r} candidate={actual!r}"
        )
    print("DIFFERENTIAL_TEST_EXIT: 1" if mismatches else "DIFFERENTIAL_TEST_EXIT: 0")
    raise SystemExit(1 if mismatches else 0)


if __name__ == "__main__":
    main()
