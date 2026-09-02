#!/usr/bin/env python3
"""Independent CPython differential test for HumanEval 126."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
from pathlib import Path


EVIDENCE = Path("/audit-output/evidence")
SCOPE_PATH = EVIDENCE / "differential_input_scope.json"
CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/candidate-src/solution.py")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_sorted


def cases(scope: dict):
    seen: set[tuple[int, ...]] = set()
    for group in ("documented_examples", "explicit_boundaries"):
        for case in scope[group]:
            key = tuple(case)
            if key not in seen:
                seen.add(key)
                yield case
    product = scope["generated_product"]
    for length in product["lengths"]:
        for values in itertools.product(product["values"], repeat=length):
            if values not in seen:
                seen.add(values)
                yield list(values)


def main() -> int:
    scope = json.loads(SCOPE_PATH.read_text())
    canonical = load_function("trusted_canonical_126", CANONICAL_PATH)
    generated = load_function("audited_generated_126", CANDIDATE_PATH)

    checked = 0
    mismatches = []
    true_count = 0
    false_count = 0
    digest = hashlib.sha256()

    for case in cases(scope):
        expected = canonical(case.copy())
        actual = generated(case.copy())
        digest.update(
            json.dumps(
                [case, expected, actual],
                separators=(",", ":"),
            ).encode()
        )
        digest.update(b"\n")
        checked += 1
        true_count += int(bool(expected))
        false_count += int(not expected)
        if type(expected) is not bool or type(actual) is not bool or actual != expected:
            mismatches.append(
                {
                    "input": case,
                    "canonical": repr(expected),
                    "generated": repr(actual),
                }
            )
            if len(mismatches) >= 20:
                break

    print(f"canonical={CANONICAL_PATH}")
    print(f"generated={CANDIDATE_PATH}")
    print(f"scope={SCOPE_PATH}")
    print(
        f"checked={checked} true={true_count} false={false_count} "
        f"mismatches={len(mismatches)}"
    )
    print(f"ordered_case_result_sha256={digest.hexdigest()}")
    if mismatches:
        print(json.dumps(mismatches, indent=2))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
