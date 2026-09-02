#!/usr/bin/env python3
"""Independent differential test for HumanEval 93 (encode)."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
import string
import sys
from pathlib import Path


def load_encode(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.encode


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: differential_test.py CANONICAL.py CANDIDATE.py", file=sys.stderr)
        return 2

    canonical = load_encode(Path(sys.argv[1]), "trusted_canonical")
    candidate = load_encode(Path(sys.argv[2]), "candidate_solution")

    examples = ["test", "This is a message"]
    empty = [""]
    branch_singletons = list(string.ascii_letters + " ")
    branch_pairs = [
        "".join(pair)
        for pair in itertools.product(string.ascii_letters, repeat=2)
    ]

    rng = random.Random(930026)
    alphabet = string.ascii_letters + " "
    generated = [
        "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 65)))
        for _ in range(5000)
    ]

    cases = examples + empty + branch_singletons + branch_pairs + generated
    encoded_corpus = json.dumps(cases, ensure_ascii=True, separators=(",", ":"))
    mismatches = []
    for index, value in enumerate(cases):
        expected = canonical(value)
        actual = candidate(value)
        if actual != expected:
            mismatches.append(
                {
                    "index": index,
                    "input": value,
                    "canonical": expected,
                    "candidate": actual,
                }
            )
            if len(mismatches) == 20:
                break

    print(f"examples={len(examples)}")
    print(f"empty_cases={len(empty)}")
    print(f"branch_singletons={len(branch_singletons)}")
    print(f"all_ascii_letter_pairs={len(branch_pairs)}")
    print(f"generated_ascii_letter_space_cases={len(generated)}")
    print(f"total_cases={len(cases)}")
    print(f"corpus_sha256={hashlib.sha256(encoded_corpus.encode()).hexdigest()}")
    print(f"mismatch_count={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches, ensure_ascii=True, indent=2))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
