#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import itertools


def load(path: str):
    spec = importlib.util.spec_from_file_location("candidate_vacuity", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.triples_sum_to_zero


values = [0, 0, 0]
summary = any(sum(triple) == 0 for triple in itertools.combinations(values, 3))
program_result = load("/tmp/audit-work/reconstruction/solution.py")(list(values))
mutated_target = not summary
print(f"witness={values}")
print(f"program_result={program_result}")
print(f"hasZeroTriple={summary}")
print(f"mutated_target_not_hasZeroTriple={mutated_target}")
assert program_result is True and summary is True and mutated_target is False
print("FALSE_MUTATION_WITNESS_CONFIRMED=true")
