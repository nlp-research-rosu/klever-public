#!/usr/bin/env python3
"""Independent candidate/canonical differential test on the promised domain."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.correct_bracketing


def independent_stack_oracle(text: str) -> bool:
    balance = 0
    for character in text:
        if character == "<":
            balance += 1
        else:
            balance -= 1
        if balance < 0:
            return False
    return balance == 0


def main() -> None:
    canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
    generated = load_entry(
        Path("/tmp/audit-work/proof/solution.py"), "scratch_generated"
    )

    named_cases = [
        ("documented-single-open", "<"),
        ("documented-pair", "<>"),
        ("documented-nested", "<<><>>"),
        ("documented-negative-prefix", "><<>"),
        ("empty", ""),
        ("single-close", ">"),
        ("positive-final-balance", "<<"),
        ("negative-on-second-step", "<>>"),
        ("balanced-nested", "<<>>"),
        ("balanced-sequential", "<><>"),
        ("negative-after-balanced-prefix", "<>>"),
        ("deep-boundary", "<" * 64 + ">" * 64),
    ]

    mismatches: list[dict[str, object]] = []
    evaluated: list[tuple[str, bool, bool, bool]] = []

    def check(text: str) -> None:
        expected = canonical(text)
        actual = generated(text)
        independent = independent_stack_oracle(text)
        evaluated.append((text, expected, actual, independent))
        if actual != expected or actual != independent:
            mismatches.append(
                {
                    "input": text,
                    "canonical": expected,
                    "generated": actual,
                    "independent": independent,
                }
            )

    print("NAMED CASES")
    for label, text in named_cases:
        check(text)
        print(
            json.dumps(
                {
                    "label": label,
                    "input": text,
                    "canonical": canonical(text),
                    "generated": generated(text),
                    "independent": independent_stack_oracle(text),
                },
                sort_keys=True,
            )
        )

    exhaustive_count = 0
    for length in range(13):
        for characters in itertools.product("<>", repeat=length):
            check("".join(characters))
            exhaustive_count += 1

    rng = random.Random(560056)
    random_count = 1000
    for _ in range(random_count):
        length = rng.randint(13, 512)
        check("".join(rng.choice("<>") for _ in range(length)))

    digest = hashlib.sha256(
        json.dumps(evaluated, separators=(",", ":")).encode()
    ).hexdigest()
    print(f"EXHAUSTIVE_SCOPE lengths=0..12 count={exhaustive_count}")
    print(
        "GENERATED_SCOPE "
        f"seed=560056 count={random_count} lengths=13..512 alphabet='<>'"
    )
    print(f"EVALUATION_DIGEST sha256={digest}")
    print(f"TOTAL_EVALUATIONS count={len(evaluated)}")
    print(f"MISMATCHES count={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches[:20], indent=2, sort_keys=True))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
