#!/usr/bin/env python3
"""Mechanical normalized-constructor comparison of solution.mpy and spec bodies."""

from __future__ import annotations

import re
from pathlib import Path


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


mpy = compact(Path("/tmp/audit-work/reconstruction/solution.mpy").read_text())
prefix = 'Module(FuncDef("sum_to_n",Params("n"),'
assert mpy.startswith(prefix) and mpy.endswith("))")
body = mpy[len(prefix) : -2]
closure = 'closureVal("n",.ParamNames,' + body + ",0)"

spec = compact(Path("/tmp/audit-work/reconstruction/spec.k").read_text())
occurrences = spec.count(closure)
assert occurrences == 2, occurrences

expected_loop = compact(
    """
    #while(Compare(Name("n"), CmpOp(">", Int(0))),
      AugAssign(Name("total"), "+", Name("n"))
      AugAssign(Name("n"), "-", Int(1)))
    """
)
assert expected_loop in spec
assert body.startswith('Assign(Name("total"),Int(0))While(')
assert body.endswith('Return(Name("total"))')

print(f"normalized_solution_body_bytes={len(body)}")
print(f"exact_closure_occurrences={occurrences}")
print("CLAIM_TERM_COMPARE_PASS")
