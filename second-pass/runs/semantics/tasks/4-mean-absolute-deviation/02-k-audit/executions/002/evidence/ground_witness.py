#!/usr/bin/env python3
"""Concrete satisfying witness for the target claim's pre/postcondition."""

from __future__ import annotations

import importlib.util


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.mean_absolute_deviation


def main() -> None:
    values = [1.0, 2.0, 3.0, 4.0]
    precondition = bool(values) and all(isinstance(value, float) for value in values)

    # Interpret the candidate's structural K fold equations using ordinary
    # Python floats, without calling either implementation.
    total = float(0)
    for value in values:
        total = total + value
    mean = total / len(values)
    deviation = 0.0
    for value in values:
        deviation = deviation + abs(value - mean)
    interpreted_formal_result = deviation / len(values)

    canonical = load("/reference/canonical.py", "ground_canonical")
    candidate = load("/tmp/audit-work/candidate/solution.py", "ground_candidate")
    canonical_result = canonical(list(values))
    candidate_result = candidate(list(values))

    print(f"input={values!r}")
    print(f"nonEmptyFloats_precondition={precondition}")
    print(f"interpreted_formal_result={interpreted_formal_result!r}")
    print(f"canonical_result={canonical_result!r}")
    print(f"candidate_result={candidate_result!r}")
    matches = interpreted_formal_result == canonical_result == candidate_result
    print(f"all_equal={matches}")
    assert precondition and matches


if __name__ == "__main__":
    main()
