#!/usr/bin/env python3
"""Auditor-authored differential test for HumanEval 86."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/anti-shuffle")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.anti_shuffle


def corpus() -> list[str]:
    cases = {
        "",
        "Hi",
        "hello",
        "Hello World!!!",
        "a",
        "ab",
        "ba",
        "aa",
        "cba",
        "abc",
        "bac",
        " ",
        "  ",
        "   ",
        " a",
        "a ",
        " a ",
        "  cba  a",
        "\t",
        "\n",
        "b\ta",
        "b\na",
        "\x00",
        "\x00 ",
        "éΩ a😀",
        "😀éΩ Ω😀é",
        chr(0x10FFFF) + "A",
    }

    # Exhaustively covers separators and all insertion comparison outcomes.
    alphabet = " aA!0~\t\n"
    for length in range(6):
        cases.update(map("".join, itertools.product(alphabet, repeat=length)))

    rng = random.Random(8600729)
    codepoints = [
        0,
        1,
        9,
        10,
        31,
        32,
        33,
        47,
        48,
        57,
        64,
        65,
        90,
        96,
        97,
        122,
        126,
        127,
        128,
        255,
        256,
        0x3A9,
        0x4E2D,
        0x1F600,
        0x10FFFF,
    ]
    random_alphabet = "".join(map(chr, codepoints))
    for _ in range(5000):
        cases.add(
            "".join(
                rng.choice(random_alphabet)
                for _ in range(rng.randrange(0, 101))
            )
        )
    return sorted(cases)


def main() -> None:
    canonical = load_entry("trusted_canonical_86", SCRATCH / "canonical.py")
    generated = load_entry("candidate_solution_86", SCRATCH / "solution.py")
    cases = corpus()
    digest = hashlib.sha256()
    mismatches = []

    examples = {
        "Hi": "Hi",
        "hello": "ehllo",
        "Hello World!!!": "Hello !!!Wdlor",
    }
    for source, expected in examples.items():
        if canonical(source) != expected or generated(source) != expected:
            mismatches.append(("documented-example", source, expected))

    for value in cases:
        encoded = value.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
        trusted = canonical(value)
        actual = generated(value)
        if trusted != actual:
            mismatches.append(("differential", value, trusted, actual))
            if len(mismatches) >= 10:
                break

        # Independently check the natural-language structure.
        expected = " ".join("".join(sorted(word)) for word in value.split(" "))
        if actual != expected:
            mismatches.append(("contract", value, expected, actual))
            if len(mismatches) >= 10:
                break

    print(f"cases={len(cases)}")
    print(f"corpus_sha256={digest.hexdigest()}")
    print(f"mismatches={len(mismatches)}")
    for mismatch in mismatches:
        print(repr(mismatch))
    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
