#!/usr/bin/env python3
"""Independent, deterministic differential test for HumanEval 86."""

import argparse
import hashlib
import importlib.util
import itertools
import json
import random
import string
import sys
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.anti_shuffle


def make_inputs():
    documented_and_boundaries = [
        "",
        " ",
        "  ",
        "   ",
        "Hi",
        "hello",
        "Hello World!!!",
        "  ba  dc ",
        "a",
        "aa",
        "ba",
        "ab",
        "cba",
        "b a",
        "a b",
        "ba ",
        " ba",
        "ba  dc",
        "zA9! 0b?",
        "\tba\n",
        "\x00ba\x00",
        "éa Ωβ",
        "🙂a 🙂!",
        "a" * 900,
        "a" * 975,
        "a" * 990,
        "a" * 995,
        "a" * 996,
        "a" * 997,
        "a" * 998,
        "a" * 999,
        "a" * 1000,
        "a" * 1001,
        "a" * 1100,
        "abcdefghijklmnopqrstuvwxyz" * 40,
    ]

    exhaustive = [
        "".join(chars)
        for length in range(0, 6)
        for chars in itertools.product(" aB!0é", repeat=length)
    ]

    rng = random.Random(860086)
    alphabet = (
        string.ascii_letters
        + string.digits
        + string.punctuation
        + " \t\n"
        + "éΩβ中🙂"
    )
    generated = [
        "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 81)))
        for _ in range(1000)
    ]

    # De-duplicate without losing deterministic order.
    return list(dict.fromkeys(documented_and_boundaries + exhaustive + generated))


def emit_inputs(inputs):
    for value in inputs:
        print(json.dumps(value, ensure_ascii=False))


def read_inputs(path: Path):
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
    ]


def summarize_outcome(outcome):
    if outcome[0] == "exception":
        return repr(outcome)
    value = outcome[1]
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return f"('value', length={len(value)}, sha256={digest})"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-inputs", action="store_true")
    parser.add_argument("--inputs", type=Path)
    parser.add_argument("--canonical", type=Path)
    parser.add_argument("--generated", type=Path)
    args = parser.parse_args()

    values = make_inputs() if args.inputs is None else read_inputs(args.inputs)
    if args.emit_inputs:
        emit_inputs(values)
        return 0

    if args.canonical is None or args.generated is None:
        parser.error("--canonical and --generated are required for testing")

    canonical = load_entry("trusted_canonical", args.canonical)
    generated = load_entry("candidate_generated", args.generated)
    mismatches = []
    for value in values:
        try:
            expected = ("value", canonical(value))
        except Exception as error:
            expected = ("exception", type(error).__name__, str(error))
        try:
            actual = ("value", generated(value))
        except Exception as error:
            actual = ("exception", type(error).__name__, str(error))
        if actual != expected:
            mismatches.append((value, expected, actual))
            if len(mismatches) <= 20:
                preview = repr(value)
                if len(preview) > 180:
                    preview = preview[:177] + "..."
                print(
                    f"MISMATCH input_length={len(value)} input_preview={preview} "
                    f"canonical={summarize_outcome(expected)} "
                    f"generated={summarize_outcome(actual)}"
                )

    encoded = "".join(
        json.dumps(v, ensure_ascii=False) + "\n" for v in values
    ).encode("utf-8")
    print(f"input_count={len(values)}")
    print(f"inputs_sha256={hashlib.sha256(encoded).hexdigest()}")
    print(f"mismatch_count={len(mismatches)}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
