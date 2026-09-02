#!/usr/bin/env python3
"""Independent differential test for HumanEval 38 decode_cyclic.

The trusted canonical implementation and the scratch copy of the submitted
implementation are imported under distinct module names.  The corpus covers
the zero-iteration and every first-loop/suffix boundary (lengths 0..6),
exhaustive short strings, Unicode/control representatives, deterministic
generated strings, and long inputs.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import random
import string
from pathlib import Path

CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path(
    "/tmp/audit-work/38-decode-cyclic-audit/candidate-src/solution.py"
)
SEED = 380038


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def corpus() -> tuple[list[str], dict[str, int]]:
    cases: list[str] = [
        "",
        "a",
        "ab",
        "abc",
        "abcd",
        "abcde",
        "abcdef",
        "abcdefg",
        "abcdefgh",
        "bca",
        "bcaefdgh",
        "\x00",
        "\x00a\x00",
        "é",
        "éß",
        "éß中",
        "🙂",
        "🙂🙃",
        "🙂🙃😉",
        "e\u0301x",
        "\n\t\r",
    ]
    boundary_count = len(cases)

    alphabet = ("a", "é", "🙂")
    exhaustive = [
        "".join(chars)
        for length in range(8)
        for chars in itertools.product(alphabet, repeat=length)
    ]
    cases.extend(exhaustive)

    rng = random.Random(SEED)
    generated_alphabet = (
        string.ascii_letters
        + string.digits
        + string.punctuation
        + " \t\n"
        + "éß中🙂🙃😉"
    )
    generated = [
        "".join(rng.choice(generated_alphabet) for _ in range(length))
        for length in range(129)
        for _ in range(25)
    ]
    cases.extend(generated)

    cases.extend(
        [
            "a" * 999,
            "ab" * 500,
            "🙂é中" * 334,
        ]
    )

    # Retain first occurrence so the preserved list is deterministic and exact.
    cases = list(dict.fromkeys(cases))
    scopes = {
        "explicit_boundary_and_special": boundary_count,
        "exhaustive_alphabet_size": len(alphabet),
        "exhaustive_lengths_0_through": 7,
        "generated_lengths_0_through": 128,
        "generated_per_length": 25,
        "long_cases": 3,
        "unique_total": len(cases),
    }
    return cases, scopes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dump-inputs", action="store_true")
    args = parser.parse_args()
    cases, scopes = corpus()
    if args.dump_inputs:
        print(json.dumps({"seed": SEED, "scopes": scopes, "inputs": cases},
                         ensure_ascii=True, separators=(",", ":")))
        return 0

    canonical = load(CANONICAL_PATH, "trusted_humaneval38")
    candidate = load(CANDIDATE_PATH, "submitted_humaneval38")

    mismatches = []
    inverse_mismatches = []
    branch_lengths = {}
    for value in cases:
        want = canonical.decode_cyclic(value)
        got = candidate.decode_cyclic(value)
        if want != got:
            mismatches.append({"input": value, "canonical": want, "candidate": got})

        encoded = canonical.encode_cyclic(value)
        decoded = candidate.decode_cyclic(encoded)
        if decoded != value:
            inverse_mismatches.append(
                {"source": value, "encoded": encoded, "decoded": decoded}
            )

        if len(value) <= 8 and len(value) not in branch_lengths:
            branch_lengths[len(value)] = {
                "input": value,
                "canonical": want,
                "candidate": got,
            }

    serialized = json.dumps(cases, ensure_ascii=True, separators=(",", ":"))
    print("oracle=/reference/canonical.py:decode_cyclic")
    print(f"candidate={CANDIDATE_PATH}:decode_cyclic")
    print("documented_decode_examples=0")
    print(f"seed={SEED}")
    print("scopes=" + json.dumps(scopes, sort_keys=True))
    print("input_list_sha256=" + hashlib.sha256(serialized.encode()).hexdigest())
    print("length_boundary_results=" +
          json.dumps(branch_lengths, ensure_ascii=True, sort_keys=True))
    print(f"direct_mismatches={len(mismatches)}")
    print(f"inverse_property_mismatches={len(inverse_mismatches)}")
    if mismatches:
        print("first_direct_mismatches=" +
              json.dumps(mismatches[:10], ensure_ascii=True))
    if inverse_mismatches:
        print("first_inverse_mismatches=" +
              json.dumps(inverse_mismatches[:10], ensure_ascii=True))
    return 1 if mismatches or inverse_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
