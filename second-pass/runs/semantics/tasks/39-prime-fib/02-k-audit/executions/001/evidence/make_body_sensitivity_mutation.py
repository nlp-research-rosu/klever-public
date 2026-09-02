#!/usr/bin/env python3
"""Materially change the submitted MPY body and add a concrete n=1 call."""

from pathlib import Path


source = Path("/candidate/solution.mpy").read_text()
needle = '    Return(Name("first"))))\n'
replacement = '    Return(Int(999))))\n'
if source.count(needle) != 1:
    raise SystemExit(f"expected one target return, found {source.count(needle)}")
mutated = source.replace(needle, replacement)

mutation_dir = Path("/tmp/audit-work/body-sensitivity")
mutation_dir.mkdir(parents=True, exist_ok=True)
(mutation_dir / "solution-mutated.mpy").write_text(mutated)
if not mutated.endswith(")\n"):
    raise SystemExit("mutated module has unexpected ending")
harness = (
    mutated[:-2]
    + '\n  Assign(Name("answer"), Call(Name("prime_fib"), Int(1)))\n)\n'
)
(mutation_dir / "solution-mutated-call.mpy").write_text(harness)
print("MUTATION Return(Name(\"first\")) -> Return(Int(999))")
print("WROTE solution-mutated.mpy and solution-mutated-call.mpy")
