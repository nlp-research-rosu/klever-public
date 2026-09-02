#!/usr/bin/env python3
"""Independent differential test for HumanEval 74 total_match."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import inspect
import json
import random
from pathlib import Path
from typing import Callable


def load_entry(path: Path, module_name: str) -> Callable[[list[str], list[str]], list[str]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    entry = getattr(module, "total_match")
    return entry


def selected_side(result: list[str], left: list[str], right: list[str]) -> str:
    if result is left:
        return "left"
    if result is right:
        return "right"
    return "neither"


parser = argparse.ArgumentParser()
parser.add_argument("canonical", type=Path)
parser.add_argument("generated", type=Path)
parser.add_argument("evidence_dir", type=Path)
args = parser.parse_args()

canonical = load_entry(args.canonical, "trusted_canonical_74")
generated = load_entry(args.generated, "candidate_solution_74")
expected_signature = "(lst1, lst2)"
for name, entry in (("canonical", canonical), ("generated", generated)):
    actual_signature = str(inspect.signature(entry))
    if actual_signature != expected_signature:
        raise AssertionError(f"{name} signature {actual_signature} != {expected_signature}")

documented = [
    ([], []),
    (["hi", "admin"], ["hI", "Hi"]),
    (["hi", "admin"], ["hi", "hi", "admin", "project"]),
    (["hi", "admin"], ["hI", "hi", "hi"]),
    (["4"], ["1", "2", "3", "4", "5"]),
]

boundaries = [
    ([], [""]),
    ([""], []),
    ([], ["a"]),
    (["a"], []),
    (["a"], ["b"]),
    (["ab"], ["c"]),
    (["c"], ["ab"]),
    (["", ""], [""]),
    (["a", ""], ["", "b"]),
    (["🙂"], ["ab"]),
    (["e\u0301"], ["é"]),
    (["\x00", "\n"], ["xy"]),
    (["a" * 1000], ["b" * 999]),
    (["a" * 999], ["b" * 1000]),
]

atoms = ["", "a", "bb", "é", "🙂"]
small_lists: list[list[str]] = [[]]
small_lists.extend([[a] for a in atoms])
small_lists.extend([[a, b] for a in atoms for b in atoms])
exhaustive = [(left, right) for left in small_lists for right in small_lists]

rng = random.Random(740074)
alphabet = ["a", "B", "0", "é", "🙂", "\u0301", "\x00"]


def random_string() -> str:
    return "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 9)))


random_cases = [
    (
        [random_string() for _ in range(rng.randrange(0, 7))],
        [random_string() for _ in range(rng.randrange(0, 7))],
    )
    for _ in range(1000)
]

cases = documented + boundaries + exhaustive + random_cases
serialized_inputs = json.dumps(
    [{"lst1": left, "lst2": right} for left, right in cases],
    ensure_ascii=True,
    separators=(",", ":"),
    sort_keys=True,
).encode()
input_digest = hashlib.sha256(serialized_inputs).hexdigest()
args.evidence_dir.mkdir(parents=True, exist_ok=True)
(args.evidence_dir / "differential_inputs.json").write_bytes(serialized_inputs + b"\n")

mismatches: list[dict[str, object]] = []
branch_counts = {"left_strict": 0, "tie": 0, "right_strict": 0}
for index, (left, right) in enumerate(cases):
    left_total = sum(map(len, left))
    right_total = sum(map(len, right))
    if left_total < right_total:
        branch_counts["left_strict"] += 1
    elif left_total == right_total:
        branch_counts["tie"] += 1
    else:
        branch_counts["right_strict"] += 1

    canonical_result = canonical(left, right)
    generated_result = generated(left, right)
    canonical_side = selected_side(canonical_result, left, right)
    generated_side = selected_side(generated_result, left, right)
    if (
        canonical_result != generated_result
        or canonical_side != generated_side
        or canonical_side == "neither"
    ):
        mismatches.append(
            {
                "index": index,
                "lst1": left,
                "lst2": right,
                "canonical_result": canonical_result,
                "generated_result": generated_result,
                "canonical_side": canonical_side,
                "generated_side": generated_side,
            }
        )

summary = {
    "canonical": str(args.canonical),
    "generated": str(args.generated),
    "signature": expected_signature,
    "documented_cases": len(documented),
    "boundary_cases": len(boundaries),
    "exhaustive_cases": len(exhaustive),
    "random_seed": 740074,
    "random_cases": len(random_cases),
    "total_cases": len(cases),
    "branch_counts": branch_counts,
    "input_sha256": input_digest,
    "mismatch_count": len(mismatches),
    "mismatches": mismatches,
}
(args.evidence_dir / "differential_results.json").write_text(
    json.dumps(summary, indent=2, ensure_ascii=True, sort_keys=True) + "\n",
    encoding="utf-8",
)
print(json.dumps(summary, indent=2, ensure_ascii=True, sort_keys=True))
raise SystemExit(1 if mismatches else 0)
