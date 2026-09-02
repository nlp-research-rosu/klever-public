#!/usr/bin/env python3
"""Generate a K claim equating the proof alias with the translated function body.

The extraction is constructor-level: the submitted MPY file must consist of one
Module containing the expected intersection FuncDef, and the exact remaining
constructor text becomes the claim RHS.
"""

import argparse
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument("--body-only", action="store_true")
parser.add_argument("--normalized-body")
arguments = parser.parse_args()

source = Path("/tmp/audit-work/reconstruction/solution.regenerated.mpy").read_text()
prefix = (
    "Module(\n"
    '  FuncDef("intersection", Params("interval1", "interval2"),\n'
)
suffix = "))\n"
assert source.startswith(prefix), "unexpected translated module/function header"
assert source.endswith(suffix), "unexpected translated module/function trailer"
body = source[len(prefix) : -len(suffix)]
assert body.strip().startswith("Assign(")
assert body.strip().endswith('Return(Str("YES"))')

if arguments.body_only:
    print(body)
    raise SystemExit(0)

if arguments.normalized_body:
    body = Path(arguments.normalized_body).read_text().strip()

print('requires "verification.k"')
print()
print("module CONSTRUCTOR-PINNING-SPEC")
print("  imports VERIFICATION-BASE")
print()
print("  claim")
print("    <k> intersectionBody ~> K:K")
print("      =>")
print(body)
print("      ~> K")
print("    </k>")
print("    [label(constructor-pinning)]")
print("endmodule")
