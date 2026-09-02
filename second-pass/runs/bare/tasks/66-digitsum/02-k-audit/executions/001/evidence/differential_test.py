#!/usr/bin/env python3
"""Independent differential test for HumanEval 66 digitSum.

The corpus is fully determined by differential_inputs.json.  The oracle and
candidate are imported from distinct source paths.  The test intentionally
keeps going after mismatches so the audit records their scope.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INPUTS_PATH = ROOT / "differential_inputs.json"
CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/reconstruction/solution.py")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def valid_random_codepoint(rng: random.Random, ranges: list[list[int]]) -> int:
    low, high = ranges[rng.randrange(len(ranges))]
    return rng.randint(low, high)


def build_corpus(config: dict) -> tuple[list[str], dict[str, int]]:
    ordered: list[str] = []
    counts: dict[str, int] = {}

    for section in (
        "documented_examples",
        "branch_and_string_boundaries",
        "unicode_uppercase_boundaries",
    ):
        values = config[section]
        counts[section] = len(values)
        ordered.extend(values)

    gen = config["generator"]
    alphabet = gen["exhaustive_alphabet"]
    exhaustive = [
        "".join(chars)
        for length in gen["exhaustive_lengths"]
        for chars in itertools.product(alphabet, repeat=length)
    ]
    counts["exhaustive_generated"] = len(exhaustive)
    ordered.extend(exhaustive)

    rng = random.Random(gen["random_seed"])
    random_values: list[str] = []
    for _ in range(gen["random_cases"]):
        length = rng.randint(gen["random_min_length"], gen["random_max_length"])
        random_values.append(
            "".join(
                chr(valid_random_codepoint(rng, gen["random_codepoint_ranges"]))
                for _ in range(length)
            )
        )
    counts["random_generated"] = len(random_values)
    ordered.extend(random_values)

    # Preserve first occurrence order while avoiding duplicate tests.
    unique = list(dict.fromkeys(ordered))
    counts["unique_total"] = len(unique)
    return unique, counts


def main() -> int:
    config = json.loads(INPUTS_PATH.read_text(encoding="utf-8"))
    canonical = load_module("trusted_humaneval_66", CANONICAL_PATH)
    candidate = load_module("submitted_solution", CANDIDATE_PATH)
    corpus, counts = build_corpus(config)

    serialized = json.dumps(
        corpus, ensure_ascii=True, separators=(",", ":")
    ).encode("ascii")
    digest = hashlib.sha256(serialized).hexdigest()

    mismatches: list[tuple[str, int, int]] = []
    for value in corpus:
        expected = canonical.digitSum(value)
        actual = candidate.digitSum(value)
        if expected != actual:
            mismatches.append((value, expected, actual))

    print("oracle=/reference/canonical.py:digitSum")
    print("candidate=/tmp/audit-work/reconstruction/solution.py:digitSum")
    print(f"counts={json.dumps(counts, sort_keys=True)}")
    print(f"corpus_json_sha256={digest}")
    print(f"mismatch_count={len(mismatches)}")
    for value, expected, actual in mismatches[:50]:
        print(
            "MISMATCH "
            + json.dumps(
                {
                    "input": value,
                    "codepoints": [ord(ch) for ch in value],
                    "canonical": expected,
                    "candidate": actual,
                },
                ensure_ascii=True,
                sort_keys=True,
            )
        )
    if len(mismatches) > 50:
        print(f"mismatches_omitted={len(mismatches) - 50}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
