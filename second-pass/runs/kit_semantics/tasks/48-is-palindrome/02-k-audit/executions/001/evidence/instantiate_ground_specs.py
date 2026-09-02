#!/usr/bin/env python3
"""Generate ground result instances from the immutable positive target claim."""

from __future__ import annotations

from pathlib import Path


SOURCE = Path("/candidate/spec.k").read_text(encoding="utf-8")
OUT = Path("/tmp/audit-work/48-is-palindrome-audit")

CASES = {
    "empty": (".IntSeq", "true"),
    "aba": ("iCons(97, iCons(98, iCons(97, .IntSeq)))", "true"),
    "ab": ("iCons(97, iCons(98, .IntSeq))", "false"),
    "emoji": ("iCons(128578, iCons(233, iCons(128578, .IntSeq)))", "true"),
}

for name, (term, expected) in CASES.items():
    module = f"SPEC-GROUND-{name.upper()}"
    label = f"ground-{name}"
    text = SOURCE
    text = text.replace("module SPEC", f"module {module}", 1)
    text = text.replace("claim [is-palindrome]:", f"claim [{label}]:", 1)
    text = text.replace("str(S:IntSeq)", f"str({term})", 1)
    expression = "S ==K buildIS(S, isLen(S) -Int 1, -1, -1)"
    if text.count(expression) != 1:
        raise AssertionError(f"unexpected result-expression count for {name}")
    text = text.replace(expression, expected, 1)
    path = OUT / f"spec-ground-{name}.k"
    path.write_text(text, encoding="utf-8")
    print(f"WROTE {path} module={module} label={label} expected={expected}")
