#!/usr/bin/env python3
"""Mutate the actual byLengthBody term while leaving bridge patterns unchanged."""

from pathlib import Path


SCRATCH = Path("/tmp/audit-work/105-by-length/recon")
source = (SCRATCH / "verification.k").read_text(encoding="utf-8")
marker = '  syntax Val ::= "byLengthClosure"'
prefix, suffix = source.split(marker, 1)
old = '''Attribute(Name("values"), "append"),
               Name("value")'''
new = '''Attribute(Name("values"), "append"),
               BinOp("+", Name("value"), Int(1))'''
assert prefix.count(old) == 1, "expected one append in the byLengthBody region"
assert suffix.count('Attribute(Name("values"), "append")') == 1
assert suffix.count('Name("value"))),') == 1
mutated = prefix.replace(old, new, 1) + marker + suffix
(SCRATCH / "body-mutated-verification.k").write_text(
    mutated, encoding="utf-8"
)
print(f"WROTE: {SCRATCH / 'body-mutated-verification.k'}")
print('MUTATION: first source loop appends value + 1 instead of value')
print('UNCHANGED: proof-local filter-loop bridge still matches append(value)')
