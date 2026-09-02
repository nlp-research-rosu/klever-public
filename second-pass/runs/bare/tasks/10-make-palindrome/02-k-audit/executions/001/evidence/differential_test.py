#!/usr/bin/env python3
"""Independent candidate-versus-canonical differential test.

The oracle and candidate are loaded from separate source paths.  The generated
short cases are exhaustive over {"a", "b", "c"} through length six.  Explicit
cases cover the supplied examples, both immediate-return and recursive control
branches, Unicode/code-point behavior, and a recursion-depth boundary.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
from typing import Any, Callable


CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/solution.py")


def load_function(path: Path, module_name: str) -> Callable[[str], str]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.make_palindrome


def outcome(function: Callable[[str], str], value: str) -> dict[str, Any]:
    try:
        result = function(value)
        encoded = result.encode("utf-8", "surrogatepass")
        return {
            "kind": "return",
            "type": type(result).__name__,
            "length": len(result),
            "sha256": hashlib.sha256(encoded).hexdigest(),
            "value": result if len(result) <= 80 else None,
        }
    except BaseException as error:
        return {
            "kind": "raise",
            "type": type(error).__name__,
            "message": str(error),
        }


def main() -> int:
    canonical = load_function(CANONICAL_PATH, "trusted_canonical")
    candidate = load_function(CANDIDATE_PATH, "audited_candidate")

    named_cases = [
        ("prompt-empty", ""),
        ("prompt-cat", "cat"),
        ("prompt-cata", "cata"),
        ("one-char-palindrome", "a"),
        ("two-char-palindrome", "aa"),
        ("first-recursive-boundary", "ab"),
        ("odd-palindrome", "xyx"),
        ("repeated-recursion", "abcd"),
        ("combining-unicode", "a\u0301b"),
        ("astral-unicode", "a🙂b"),
        ("embedded-nul", "a\x00b"),
        ("recursion-limit-boundary", "a" * 1200 + "b"),
    ]

    generated = [
        "".join(chars)
        for length in range(7)
        for chars in itertools.product("abc", repeat=length)
    ]

    mismatches: list[dict[str, Any]] = []
    for name, value in named_cases:
        oracle_result = outcome(canonical, value)
        candidate_result = outcome(candidate, value)
        record = {
            "name": name,
            "input_length": len(value),
            "oracle": oracle_result,
            "candidate": candidate_result,
            "match": oracle_result == candidate_result,
        }
        print(json.dumps(record, ensure_ascii=True, sort_keys=True))
        if not record["match"]:
            mismatches.append(record)

    generated_mismatches = 0
    for value in generated:
        if outcome(canonical, value) != outcome(candidate, value):
            generated_mismatches += 1

    summary = {
        "named_case_count": len(named_cases),
        "generated_alphabet": "abc",
        "generated_max_length": 6,
        "generated_case_count": len(generated),
        "generated_mismatch_count": generated_mismatches,
        "named_mismatch_count": len(mismatches),
        "named_mismatches": [record["name"] for record in mismatches],
    }
    print("SUMMARY " + json.dumps(summary, sort_keys=True))
    return 1 if mismatches or generated_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
