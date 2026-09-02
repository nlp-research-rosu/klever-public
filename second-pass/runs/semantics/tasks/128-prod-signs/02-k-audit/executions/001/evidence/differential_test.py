#!/usr/bin/env python3
"""Independent differential and contract-oracle test for HumanEval 128."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.prod_signs


def contract_oracle(arr: list[int]):
    if not arr:
        return None
    magnitude = sum(abs(value) for value in arr)
    sign = 1
    for value in arr:
        if value == 0:
            sign = 0
        elif value < 0:
            sign = -sign
    return magnitude * sign


def same_result(left, right) -> bool:
    return type(left) is type(right) and left == right


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} OUTPUT_DIRECTORY", file=sys.stderr)
        return 64

    output_dir = Path(sys.argv[1])
    output_dir.mkdir(parents=True, exist_ok=True)

    canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
    generated = load_entry(
        Path("/tmp/audit-work/128-prod-signs.HMXf22/solution.py"),
        "candidate_solution",
    )

    named = [
        ("documented-negative", [1, 2, 2, -4]),
        ("documented-zero", [0, 1]),
        ("documented-empty", []),
        ("positive-boundary", [1]),
        ("negative-boundary", [-1]),
        ("zero-boundary", [0]),
        ("negative-then-positive", [-1, 1]),
        ("positive-then-negative", [1, -1]),
        ("all-loop-branches", [-1, 0, 1]),
        ("even-negative-parity", [-2, -3]),
        ("odd-negative-parity", [-2, -3, -4]),
        ("zero-after-negatives", [-2, -3, 0]),
        ("large-positive", [10**100]),
        ("large-negative", [-(10**100)]),
        ("large-mixed", [10**100, -(10**99), 0, -7]),
        ("long", [(-1 if i % 3 == 0 else i) for i in range(250)]),
    ]

    cases: list[tuple[str, list[int]]] = list(named)
    for length in range(0, 6):
        for values in itertools.product(range(-3, 4), repeat=length):
            cases.append((f"exhaustive-small-len-{length}", list(values)))

    rng = random.Random(128)
    for index in range(1000):
        length = rng.randrange(0, 21)
        values = [rng.randint(-1_000_000, 1_000_000) for _ in range(length)]
        cases.append((f"seeded-random-{index}", values))

    input_path = output_dir / "differential-inputs.jsonl"
    mismatch_path = output_dir / "differential-mismatches.jsonl"
    mismatch_count = 0
    canonical_mutations = 0
    generated_mutations = 0

    with input_path.open("w", encoding="utf-8") as inputs, mismatch_path.open(
        "w", encoding="utf-8"
    ) as mismatches:
        for index, (group, values) in enumerate(cases):
            inputs.write(
                json.dumps(
                    {"index": index, "group": group, "input": values},
                    separators=(",", ":"),
                )
                + "\n"
            )

            before = list(values)
            canonical_result = canonical(values)
            canonical_mutations += values != before
            values = list(before)
            generated_result = generated(values)
            generated_mutations += values != before
            oracle_result = contract_oracle(before)

            if not (
                same_result(canonical_result, generated_result)
                and same_result(canonical_result, oracle_result)
            ):
                mismatch_count += 1
                mismatches.write(
                    json.dumps(
                        {
                            "index": index,
                            "group": group,
                            "input": before,
                            "canonical": canonical_result,
                            "generated": generated_result,
                            "oracle": oracle_result,
                        },
                        separators=(",", ":"),
                    )
                    + "\n"
                )

    input_digest = hashlib.sha256(input_path.read_bytes()).hexdigest()
    summary = {
        "documented_and_boundary_cases": len(named),
        "exhaustive_small_domain": sum(7**length for length in range(6)),
        "seeded_random_cases": 1000,
        "total_cases": len(cases),
        "mismatches": mismatch_count,
        "canonical_input_mutations": canonical_mutations,
        "generated_input_mutations": generated_mutations,
        "inputs_sha256": input_digest,
    }
    (output_dir / "differential-summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, sort_keys=True))
    return 1 if mismatch_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
