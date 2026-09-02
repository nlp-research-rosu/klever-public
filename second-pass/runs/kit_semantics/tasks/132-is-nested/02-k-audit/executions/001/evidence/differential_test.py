#!/usr/bin/env python3
"""Independent canonical-versus-candidate differential test for HumanEval 132."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import random
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/132-is-nested-review/solution.py")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_nested


def direct_subsequence_oracle(value: str) -> bool:
    """Definition independent of both implementations: search four indices."""
    return any(
        value[i] == "["
        and value[j] == "["
        and value[k] == "]"
        and value[l] == "]"
        for i in range(len(value))
        for j in range(i + 1, len(value))
        for k in range(j + 1, len(value))
        for l in range(k + 1, len(value))
    )


def main() -> int:
    canonical = load_entry(CANONICAL_PATH, "trusted_humaneval_132")
    candidate = load_entry(CANDIDATE_PATH, "audited_candidate_132")

    documented = {
        "[[]]": True,
        "[]]]]]]][[[[[]": False,
        "[][]": False,
        "[]": False,
        "[[][]]": True,
        "[[]][[": True,
    }
    branch_boundaries = [
        "",
        "]",
        "[",
        "[]",
        "][",
        "[[",
        "[][",
        "[[]",
        "[[][",
        "[[]]",
        "[[]][",
        "[[]]]",
        "]]][[]]",
        "[[[[]]]]",
    ]
    exhaustive_small = [
        "".join(characters)
        for size in range(13)
        for characters in itertools.product("[]", repeat=size)
    ]
    generator = random.Random(132)
    generated_long = [
        "".join(generator.choice("[]") for _ in range(size))
        for size in (13, 14, 15, 16, 17, 31, 32, 33, 63, 64, 65, 127, 128)
        for _ in range(8)
    ]

    ordered: list[str] = []
    seen: set[str] = set()
    for value in list(documented) + branch_boundaries + exhaustive_small + generated_long:
        if value not in seen:
            ordered.append(value)
            seen.add(value)

    failures: list[tuple[str, object, object, object]] = []
    for value in ordered:
        trusted_result = canonical(value)
        candidate_result = candidate(value)
        definition_result = direct_subsequence_oracle(value)
        if (
            trusted_result != candidate_result
            or trusted_result != definition_result
            or type(trusted_result) is not bool
            or type(candidate_result) is not bool
        ):
            failures.append(
                (value, trusted_result, candidate_result, definition_result)
            )

    documented_failures = [
        (value, candidate(value), expected)
        for value, expected in documented.items()
        if candidate(value) != expected or canonical(value) != expected
    ]
    corpus_bytes = b"".join(
        len(value).to_bytes(4, "big") + value.encode("ascii") for value in ordered
    )
    print("trusted_entry=/reference/canonical.py:is_nested")
    print(
        "candidate_entry="
        "/tmp/audit-work/132-is-nested-review/solution.py:is_nested"
    )
    print("independent_oracle=ordered four-index search for [ [ ] ]")
    print(f"documented_examples={len(documented)}")
    print(f"branch_boundary_inputs={len(branch_boundaries)}")
    print(f"exhaustive_small_domain=all bracket strings of lengths 0..12")
    print(f"generated_long_inputs={len(generated_long)} seed=132 lengths=13..128")
    print(f"unique_inputs={len(ordered)}")
    print(f"input_corpus_sha256={hashlib.sha256(corpus_bytes).hexdigest()}")
    print(f"documented_failures={len(documented_failures)}")
    print(f"differential_or_definition_failures={len(failures)}")
    if documented_failures:
        print(f"first_documented_failures={documented_failures[:10]!r}")
    if failures:
        print(f"first_failures={failures[:10]!r}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
