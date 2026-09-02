#!/usr/bin/env python3
"""Independent canonical-vs-candidate differential for HumanEval/89."""

from __future__ import annotations

import importlib.util
import random
import sys
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.encrypt


def escaped(value: str) -> str:
    return ascii(value)


def main() -> None:
    work = Path("/tmp/audit-work/reconstruction")
    canonical = load_entry(work / "canonical.py", "trusted_canonical")
    candidate = load_entry(work / "solution.py", "generated_candidate")

    documented = ["hi", "asdfghjkl", "gf", "et"]
    boundaries = [
        "",
        "`az{",
        "vwxyz",
        "VWXYZ",
        "a",
        "v",
        "w",
        "x",
        "y",
        "z",
        "\x00",
        "\x60",
        "\x61",
        "\x7a",
        "\x7b",
        "\x7f",
        "a z!",
        "Hello, World!",
        "éclair λ中🙂",
        "\ud800",
        "\udfff",
    ]
    one_codepoint_cases = [chr(codepoint) for codepoint in range(0x110000)]

    rng = random.Random(8904)
    alphabet = [
        "\x00",
        " ",
        "`",
        "a",
        "v",
        "w",
        "x",
        "y",
        "z",
        "{",
        "A",
        "Z",
        "0",
        "9",
        "!",
        "é",
        "λ",
        "中",
        "🙂",
        "\ud800",
        "\udfff",
    ]
    generated = [
        "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 129)))
        for _ in range(2500)
    ]
    generated.extend(
        [
            "a" * 4096,
            "wxyz" * 1024,
            "".join(chr(code) for code in range(128)),
            "".join(chr(code) for code in range(0x10FF00, 0x110000)),
        ]
    )

    cases = documented + boundaries + one_codepoint_cases + generated
    mismatches = []
    for index, value in enumerate(cases):
        expected = canonical(value)
        actual = candidate(value)
        if actual != expected:
            mismatches.append((index, escaped(value), escaped(expected), escaped(actual)))
            if len(mismatches) == 20:
                break

    print(f"documented_cases={len(documented)}")
    print(f"boundary_cases={len(boundaries)}")
    print(f"all_single_codepoint_strings={len(one_codepoint_cases)}")
    print(f"seeded_generated_and_long_cases={len(generated)}")
    print(f"total_cases={len(cases)}")
    print(f"mismatches={len(mismatches)}")
    for mismatch in mismatches:
        print("mismatch", mismatch)

    for example in documented:
        print(
            "example",
            escaped(example),
            "canonical=",
            escaped(canonical(example)),
            "candidate=",
            escaped(candidate(example)),
        )
    for boundary in boundaries[:18]:
        print(
            "boundary",
            escaped(boundary),
            "canonical=",
            escaped(canonical(boundary)),
            "candidate=",
            escaped(candidate(boundary)),
        )

    if mismatches:
        sys.exit(1)
    print("DIFFERENTIAL_CHECK=PASS")


if __name__ == "__main__":
    main()
