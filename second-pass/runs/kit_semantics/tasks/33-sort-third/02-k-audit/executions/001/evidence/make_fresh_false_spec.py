#!/usr/bin/env python3
"""Create the auditor's fresh false result mutation on a satisfying input."""

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
# Deliberately false at unchanged source index 1: real value 6, mutated value 999.
false_result = (
    "vCons(2, vCons(999, vCons(3, vCons(4, vCons(8, "
    "vCons(9, vCons(5, .ValSeq)))))))"
)
prefix = prefix.replace("module SPEC", "module SPEC-FRESH-FALSE", 1)
target = re.sub(r"\bVS\b", ground, target)
target = target.replace(
    f"2 |-> list(sortThirdResult({ground}))",
    f"2 |-> list({false_result})",
    1,
)
mutated = prefix + "  claim [sort-third-fresh-false]:" + target
destination = SCRATCH / "spec-fresh-false.k"
destination.write_text(mutated, encoding="utf-8")
print(f"satisfying_input={ground}")
print(f"false_result={false_result}")
print("witness_reason=index 1 is not divisible by 3 and must remain 6, not 999")
print(f"output={destination}")
print(
    "false_result_replacement="
    + str(f"2 |-> list({false_result})" in mutated)
)
