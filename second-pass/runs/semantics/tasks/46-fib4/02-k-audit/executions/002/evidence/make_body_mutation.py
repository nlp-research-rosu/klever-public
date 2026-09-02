#!/usr/bin/env python3
"""Create a body-sensitivity spec that changes the executed closure itself."""

from pathlib import Path


ROOT = Path("/tmp/audit-work/46-fib4-review")
source = (ROOT / "spec.k").read_text()
marker = '"fib4" |-> closureVal('
start = source.index(marker)
needle = (
    'If(Compare(Name("n"), CmpOp("==", Int(2))),\n'
    '            Return(Int(2)) .Stmts,'
)
position = source.index(needle, start)
mutated = source[:position] + source[position:].replace(
    needle,
    (
        'If(Compare(Name("n"), CmpOp("==", Int(2))),\n'
        '            Return(Int(3)) .Stmts,'
    ),
    1,
)
mutated = mutated.replace(
    "module FIB4-SPEC",
    "module FIB4-SPEC-BODY-MUTATION",
    1,
)
output = ROOT / "spec-body-mutation.k"
output.write_text(mutated)
print(f"closure_marker_offset={start}")
print(f"mutated_body_offset={position}")
print("mutation=executed closure fib4(2) return changed from 2 to 3")
print("asserted expected fib4(2)=2 left unchanged")
print(f"output={output}")
