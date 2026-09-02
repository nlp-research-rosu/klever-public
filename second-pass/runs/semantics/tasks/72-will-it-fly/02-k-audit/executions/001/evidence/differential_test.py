#!/usr/bin/env python3
"""Independent differential test for HumanEval 72 `will_it_fly`.

The case stream is deterministic and is itself the preserved input
specification:

* the four documented examples plus explicit empty/boundary/negative cases;
* every list of length 0..5 over {-2,-1,0,1,2}, each tested just below, at,
  and just above its sum, plus w in {-5,0,5};
* 2,000 seeded representative lists of length 0..20 over [-100,100], with a
  rotating choice of threshold and unrelated integer weight.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path
from typing import Any, Callable, Iterable


def load_entry(path: Path, module_name: str) -> Callable[[list[int], int], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.will_it_fly


def cases() -> Iterable[tuple[list[int], int, str]]:
    explicit = [
        ([1, 2], 5, "documented-unbalanced"),
        ([3, 2, 3], 1, "documented-overweight"),
        ([3, 2, 3], 9, "documented-true"),
        ([3], 5, "documented-singleton"),
        ([], -1, "empty-overweight"),
        ([], 0, "empty-at-boundary"),
        ([], 1, "empty-underweight"),
        ([0], -1, "singleton-overweight"),
        ([0], 0, "singleton-at-boundary"),
        ([4, -10, 4], -3, "negative-sum-overweight"),
        ([4, -10, 4], -2, "negative-sum-at-boundary"),
        ([1, 2, 2, 1], 5, "even-palindrome-overweight"),
        ([1, 2, 2, 1], 6, "even-palindrome-at-boundary"),
        ([1, 2, 3, 1], 100, "within-weight-unbalanced"),
    ]
    yield from explicit

    alphabet = (-2, -1, 0, 1, 2)
    for length in range(6):
        for values in itertools.product(alphabet, repeat=length):
            q = list(values)
            total = sum(q)
            for w in sorted({total - 1, total, total + 1, -5, 0, 5}):
                yield q, w, f"exhaustive-len-{length}"

    rng = random.Random(720072)
    for index in range(2000):
        q = [rng.randint(-100, 100) for _ in range(rng.randint(0, 20))]
        total = sum(q)
        selector = index % 4
        if selector == 0:
            w = total - 1
        elif selector == 1:
            w = total
        elif selector == 2:
            w = total + 1
        else:
            w = rng.randint(-2000, 2000)
        yield q, w, "seeded-generated"


def outcome(fn: Callable[[list[int], int], bool], q: list[int], w: int) -> Any:
    try:
        return ("return", fn(list(q), w))
    except Exception as err:  # pragma: no cover - retained to compare failures
        return ("raise", type(err).__name__, str(err))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("canonical", type=Path)
    parser.add_argument("generated", type=Path)
    args = parser.parse_args()

    canonical = load_entry(args.canonical, "trusted_canonical")
    generated = load_entry(args.generated, "generated_solution")
    digest = hashlib.sha256()
    count = 0
    labels: dict[str, int] = {}
    mismatches: list[dict[str, Any]] = []

    for q, w, label in cases():
        encoded = json.dumps([q, w, label], separators=(",", ":")).encode()
        digest.update(encoded + b"\n")
        labels[label] = labels.get(label, 0) + 1
        expected = outcome(canonical, q, w)
        actual = outcome(generated, q, w)
        count += 1
        if expected != actual and len(mismatches) < 20:
            mismatches.append(
                {"q": q, "w": w, "label": label,
                 "canonical": expected, "generated": actual}
            )

    print(f"canonical={args.canonical}")
    print(f"generated={args.generated}")
    print(f"case_count={count}")
    print(f"case_stream_sha256={digest.hexdigest()}")
    print("label_counts=" + json.dumps(labels, sort_keys=True))
    print(f"mismatch_count={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches, sort_keys=True))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
