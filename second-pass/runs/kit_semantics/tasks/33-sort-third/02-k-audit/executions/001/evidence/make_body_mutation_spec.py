#!/usr/bin/env python3
"""Mutate the actual entry-claim program body while preserving its expected result."""

from __future__ import annotations

import pathlib
import re


SCRATCH = pathlib.Path("/tmp/audit-work/33-sort-third")
source = (SCRATCH / "spec.k").read_text(encoding="utf-8")
marker = "  claim [sort-third]:"
prefix, target = source.split(marker, 1)
ground = (
    "vCons(5, vCons(6, vCons(3, vCons(4, vCons(8, "
    "vCons(9, vCons(2, .ValSeq)))))))"
)
expected = (
    "vCons(2, vCons(6, vCons(3, vCons(4, vCons(8, "
    "vCons(9, vCons(5, .ValSeq)))))))"
)
prefix = prefix.replace("module SPEC", "module SPEC-BODY-MUTATION", 1)
target = re.sub(r"\bVS\b", ground, target)
target = target.replace(
    f"2 |-> list(sortThirdResult({ground}))",
    f"2 |-> list({expected})",
    1,
)
old_branch = 'BinOp("%", Name("i"), Int(3))'
new_branch = 'BinOp("%", Name("i"), Int(2))'
mutation_count = target.count(old_branch)
target = target.replace(old_branch, new_branch)
mutated = prefix + "  claim [sort-third-body-mutation]:" + target
destination = SCRATCH / "spec-body-mutation.k"
destination.write_text(mutated, encoding="utf-8")
print(f"satisfying_input={ground}")
print("body_mutation=branch predicate i % 3 == 0 changed to i % 2 == 0")
print(f"mutated_constructor_occurrences={mutation_count}")
print("expected_original_result=[2, 6, 3, 4, 8, 9, 5]")
print("actual_mutated_result=[2, 6, 2, 4, 4, 9, 5]")
print(f"output={destination}")
raise SystemExit(0 if mutation_count == 2 else 1)
