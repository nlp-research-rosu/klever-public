#!/usr/bin/env python3
from pathlib import Path

source = Path("/tmp/audit-work/source/verification.k").read_text(encoding="utf-8")
old_module = "module ORDER-BY-POINTS-VERIFICATION"
old_return = '    Return(Name("total"))'
assert source.count(old_module) == 1
assert source.count(old_return) == 1
mutated = source.replace(
    old_module,
    "module ORDER-BY-POINTS-VERIFICATION-BODY-MUTATED",
).replace(
    old_return,
    "    Return(Int(999))",
)
print(mutated, end="")
