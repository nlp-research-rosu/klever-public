#!/usr/bin/env python3
"""Create the reviewer's fresh false-result mutation."""

from pathlib import Path


ROOT = Path("/tmp/audit-work/46-fib4-review")
source = (ROOT / "spec.k").read_text()
closure_marker = source.index('"fib4" |-> closureVal(')
prefix = source[:closure_marker]
suffix = source[closure_marker:]
needle = (
    'Assert(Compare(Call(Name("fib4"), Int(12)), '
    'CmpOp("==", Int(386))))'
)
replacement = (
    'Assert(Compare(Call(Name("fib4"), Int(12)), '
    'CmpOp("==", Int(387))))'
)
if prefix.count(needle) != 1:
    raise ValueError(
        f"expected one pre-closure result obligation, found {prefix.count(needle)}"
    )
mutated = prefix.replace(needle, replacement, 1) + suffix
mutated = mutated.replace(
    "module FIB4-SPEC",
    "module FIB4-SPEC-VACUITY",
    1,
)
output = ROOT / "spec-vacuity-review.k"
output.write_text(mutated)
print(f"closure_marker_offset={closure_marker}")
print("mutation=fib4(12) expected result changed from 386 to false value 387")
print("executed closure body unchanged")
print("satisfying_precondition=the exact concrete module environment in operational-cases")
print(f"witness=Python candidate fib4(12)=386")
print(f"output={output}")
