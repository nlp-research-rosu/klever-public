#!/usr/bin/env python3
"""Create a proof definition whose executed prime_fib body returns 0."""

from pathlib import Path

work = Path("/tmp/audit-work/prime-fib-audit")
source = (work / "verification.k").read_text()
old_module = "module PRIME-FIB-VERIFICATION"
new_module = "module PRIME-FIB-VERIFICATION-BODY-MUTANT"
old_body = '         Return(Name("first")),\n         0)'
new_body = '         Return(Int(0)),\n         0)'
if source.count(old_module) != 1 or source.count(old_body) != 1:
    raise SystemExit("expected unique module name and return term")
mutant = source.replace(old_module, new_module).replace(old_body, new_body)
(work / "verification-body-mutant.k").write_text(mutant)
print("changed executed primeFibClosure body Return(Name(\"first\")) to Return(Int(0))")
