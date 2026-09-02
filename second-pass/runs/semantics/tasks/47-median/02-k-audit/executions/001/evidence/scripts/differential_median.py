#!/usr/bin/env python3
"""Independent differential test for trusted canonical.py vs candidate solution.py."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import random
from collections import Counter
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.median


def outcome(function, argument):
    try:
        value = function(list(argument))
        return {"kind": "return", "type": type(value).__name__, "value": value}
    except Exception as error:  # Compare observable exception classes as outcomes.
        return {"kind": "exception", "type": type(error).__name__}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--generated", type=Path, required=True)
    parser.add_argument("--inputs-output", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_entry("trusted_canonical", args.canonical)
    generated = load_entry("candidate_generated", args.generated)

    cases = [
        {"id": "documented-odd", "source": "prompt", "input": [3, 1, 2, 4, 5]},
        {
            "id": "documented-even",
            "source": "prompt",
            "input": [-10, 4, 6, 1000, 10, 20],
        },
        {"id": "boundary-empty", "source": "boundary", "input": []},
        {"id": "boundary-len1", "source": "boundary", "input": [7]},
        {"id": "boundary-len2", "source": "boundary", "input": [4, 1]},
        {"id": "boundary-len3", "source": "boundary", "input": [9, -2, 4]},
        {"id": "boundary-len4", "source": "boundary", "input": [4, 1, 3, 2]},
        {"id": "boundary-len5", "source": "boundary", "input": [5, 1, 4, 2, 3]},
        {"id": "boundary-len6", "source": "boundary", "input": [0, 1, 2, 3, 4, 99]},
    ]

    alphabet = (-2, -1, 0, 1, 2)
    for length in range(7):
        for index, values in enumerate(itertools.product(alphabet, repeat=length)):
            cases.append(
                {
                    "id": f"exhaustive-len{length}-{index}",
                    "source": "exhaustive",
                    "input": list(values),
                }
            )

    generator = random.Random(47047)
    for index in range(2000):
        length = generator.randrange(0, 21)
        cases.append(
            {
                "id": f"generated-{index}",
                "source": "seed-47047",
                "input": [generator.randint(-1000, 1000) for _ in range(length)],
            }
        )

    args.inputs_output.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(cases, sort_keys=True, separators=(",", ":")).encode()
    manifest_bytes = encoded + b"\n"
    args.inputs_output.write_bytes(manifest_bytes)

    mismatches = []
    mismatches_by_length = Counter()
    outcomes_by_source = Counter()
    for case in cases:
        expected = outcome(canonical, case["input"])
        actual = outcome(generated, case["input"])
        outcomes_by_source[(case["source"], "cases")] += 1
        if expected != actual:
            mismatches_by_length[len(case["input"])] += 1
            if len(mismatches) < 20:
                mismatches.append(
                    {
                        "id": case["id"],
                        "input": case["input"],
                        "canonical": expected,
                        "generated": actual,
                    }
                )

    print(f"canonical={args.canonical}")
    print(f"generated={args.generated}")
    print(f"input_manifest={args.inputs_output}")
    print(f"input_manifest_sha256={hashlib.sha256(manifest_bytes).hexdigest()}")
    print(f"case_count={len(cases)}")
    print(
        "source_counts="
        + json.dumps(
            {source: count for (source, _), count in sorted(outcomes_by_source.items())},
            sort_keys=True,
        )
    )
    print(f"mismatch_count={sum(mismatches_by_length.values())}")
    print("mismatches_by_length=" + json.dumps(dict(sorted(mismatches_by_length.items()))))
    print("first_mismatches=" + json.dumps(mismatches, sort_keys=True))
    return 1 if mismatches_by_length else 0


if __name__ == "__main__":
    raise SystemExit(main())
