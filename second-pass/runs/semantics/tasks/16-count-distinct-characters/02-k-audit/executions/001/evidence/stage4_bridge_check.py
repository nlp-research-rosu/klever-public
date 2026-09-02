#!/usr/bin/env python3
"""Compare the formal postcondition's supplied string model with CPython."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.count_distinct_characters


def k_lower_code(code: int) -> int:
    # Exact lowerC equations from the supplied semantics/methods.k.
    return code + 32 if 65 <= code <= 90 else code


def formal_postcondition(value: str) -> int:
    # Exact isLen(dedupCodes(mapLower(CS))) value, with CS = Python ords.
    lowered = [k_lower_code(code) for code in map(ord, value)]
    return len(dict.fromkeys(lowered))


def main() -> int:
    canonical = load(Path("/reference/canonical.py"), "trusted_canonical_stage4")
    generated = load(
        Path("/tmp/audit-work/candidate-src/solution.py"), "submitted_stage4"
    )
    cases = [
        "",
        "xyzXYZ",
        "Jerry",
        "AaBbCcAa",
        "123!123!",
        "\u0130",
        "Σσς",
        "\u1e9eß",
        "\U00010400\U00010428",
    ]
    model_mismatches = 0
    for value in cases:
        row = {
            "input": value,
            "code_points": list(map(ord, value)),
            "formal_postcondition": formal_postcondition(value),
            "canonical_python": canonical(value),
            "submitted_python": generated(value),
        }
        row["formal_matches_python"] = (
            row["formal_postcondition"] == row["canonical_python"]
        )
        model_mismatches += not row["formal_matches_python"]
        print(json.dumps(row, ensure_ascii=True, sort_keys=True))
    print(f"cases: {len(cases)}")
    print(f"formal-model/Python mismatches: {model_mismatches}")
    # The script succeeds when it completed; mismatches are the measured result.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
