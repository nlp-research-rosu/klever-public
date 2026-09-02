#!/usr/bin/env python3
"""Add concrete top-level calls to a translated MPY Module."""

from pathlib import Path


source = Path("/tmp/audit-work/work/solution.regenerated.mpy")
target = Path("/tmp/audit-work/work/concrete-audit.mpy")
text = source.read_text()
if not text.endswith(")\n"):
    raise SystemExit("translated module does not end in the expected close parenthesis")

calls = [0, 1, 5, 11]
suffix = "".join(
    f'  Assign(Name("answer_{n}"), Call(Name("prime_fib"), Int({n})))\n'
    for n in calls
)
target.write_text(text[:-2] + "\n" + suffix + ")\n")
print(f"WROTE {target}")
print(f"INPUTS {calls}")
