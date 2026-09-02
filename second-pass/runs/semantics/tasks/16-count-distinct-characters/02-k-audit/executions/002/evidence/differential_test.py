#!/usr/bin/env python3
"""Independent CPython differential test for HumanEval/16."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_function(module_path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.count_distinct_characters


def build_cases() -> tuple[list[str], dict[str, int]]:
    documented_and_boundaries = [
        "",
        "xyzXYZ",
        "Jerry",
        "A",
        "Z",
        "a",
        "z",
        "@A[",
        "`a{",
        "AaBbCcAa",
        "123!123!",
        "\x00A\x00a",
        "line\nLINE\t",
        "Σσς",
        "İ",
        "i\u0307",
        "ẞß",
        "éÉe\u0301E\u0301",
        "🙂🙃🙂",
        "𐐀𐐨",
    ]

    alphabet = ["@", "A", "Z", "[", "`", "a", "z", "{", "0", "!", "Σ", "ς"]
    exhaustive = [
        "".join(chars)
        for length in range(4)
        for chars in itertools.product(alphabet, repeat=length)
    ]

    generator = random.Random(0x16C0DE)
    pool = [
        "\x00",
        "A",
        "Z",
        "a",
        "z",
        "0",
        "!",
        " ",
        "\n",
        "Σ",
        "σ",
        "ς",
        "İ",
        "ß",
        "ẞ",
        "é",
        "\u0301",
        "🙂",
        "𐐀",
        "𐐨",
    ]
    generated = [
        "".join(generator.choice(pool) for _ in range(generator.randrange(0, 25)))
        for _ in range(3000)
    ]

    cases = list(
        dict.fromkeys(documented_and_boundaries + exhaustive + generated)
    )
    scope = {
        "documented_and_boundary": len(documented_and_boundaries),
        "exhaustive_ascii_unicode_boundary_alphabet_len_le_3": len(exhaustive),
        "seeded_generated": len(generated),
        "unique_total": len(cases),
    }
    return cases, scope


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("canonical", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--cases-out", required=True, type=Path)
    args = parser.parse_args()

    canonical = load_function(args.canonical, "trusted_canonical")
    candidate = load_function(args.candidate, "generated_candidate")
    cases, scope = build_cases()
    args.cases_out.write_text(
        json.dumps({"scope": scope, "inputs": cases}, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )

    mismatches = []
    for string in cases:
        expected = canonical(string)
        actual = candidate(string)
        if actual != expected:
            mismatches.append(
                {"input": string, "canonical": expected, "candidate": actual}
            )

    print(json.dumps(scope, sort_keys=True))
    print(f"MISMATCHES: {len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches[:20], ensure_ascii=False, indent=2))
        return 1
    print("DIFFERENTIAL_RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
