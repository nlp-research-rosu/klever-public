#!/usr/bin/env python3
"""Ground substitutions for the entry claim's gradeAcc result."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.numerical_letter_grade


def formal_grade_value(value):
    if value == 4.0:
        return "A+"
    if value > 3.7:
        return "A"
    if value > 3.3:
        return "A-"
    if value > 3.0:
        return "B+"
    if value > 2.7:
        return "B"
    if value > 2.3:
        return "B-"
    if value > 2.0:
        return "C+"
    if value > 1.7:
        return "C"
    if value > 1.3:
        return "C-"
    if value > 1.0:
        return "D+"
    if value > 0.7:
        return "D"
    if value > 0.0:
        return "D-"
    return "E"


def formal_grade_acc(accumulator, remaining):
    result = list(accumulator)
    for value in remaining:
        result.append(formal_grade_value(value))
    return result


def main() -> int:
    canonical = load(Path("/reference/canonical.py"), "canonical_ground")
    generated = load(Path("/candidate/solution.py"), "generated_ground")
    witnesses = {
        "empty": [],
        "documented": [4.0, 3, 1.7, 2, 3.5],
        "all-outcomes": [
            4.0, 3.8, 3.7, 3.4, 3.0, 2.8, 2.4,
            2.1, 1.8, 1.4, 1.1, 0.8, 0.1, 0.0,
        ],
    }
    for name, values in witnesses.items():
        formal = formal_grade_acc([], values)
        canonical_result = canonical(list(values))
        generated_result = generated(list(values))
        assert formal == canonical_result == generated_result
        print(f"{name}: input={values}")
        print(f"{name}: gradeAcc(.ValSeq, VS)={formal}")
        print(f"{name}: canonical={canonical_result}")
        print(f"{name}: generated={generated_result}")
    print("all_ground_substitutions_match=True")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
