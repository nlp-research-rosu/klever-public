#!/usr/bin/env python3
"""Compare selected satisfying-input theorem substitutions with both Python bodies."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def claimed_codes(strings: list[str]) -> list[int]:
    # Ground instances use ASCII code sequences, exactly the K seqConcat fold.
    codes: list[int] = []
    for value in strings:
        codes.extend(ord(char) for char in value)
    return codes


def main() -> int:
    canonical = load("canonical_witness", "/reference/canonical.py")
    candidate = load("candidate_witness", "/candidate/solution.py")
    cases = [[], ["q"], ["", "ab", "c"]]
    rows = []
    mismatch = False
    for values in cases:
        codes = claimed_codes(values)
        claimed = "".join(chr(code) for code in codes)
        canonical_value = canonical.concatenate(values)
        candidate_value = candidate.concatenate(values)
        ok = claimed == canonical_value == candidate_value
        mismatch |= not ok
        rows.append(
            {
                "input": values,
                "k_claimed_codes": codes,
                "k_claimed_string": claimed,
                "canonical": canonical_value,
                "candidate": candidate_value,
                "all_equal": ok,
            }
        )
    print(json.dumps({"witnesses": rows, "mismatch": mismatch}, indent=2))
    return 1 if mismatch else 0


if __name__ == "__main__":
    raise SystemExit(main())
