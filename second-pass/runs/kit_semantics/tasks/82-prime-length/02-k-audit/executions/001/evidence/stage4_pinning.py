#!/usr/bin/env python3
"""Mechanical constructor pinning and concrete theorem substitutions."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.prime_length


def remove_k_whitespace(text: str) -> str:
    """Remove layout outside K string tokens, preserving their exact contents."""
    result: list[str] = []
    quoted = False
    escaped = False
    for char in text:
        if quoted:
            result.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
            result.append(char)
        elif not char.isspace():
            result.append(char)
    assert not quoted
    return "".join(result)


def balanced_contents(text: str, open_index: int) -> str:
    assert text[open_index] == "("
    depth = 0
    quoted = False
    escaped = False
    for index in range(open_index, len(text)):
        char = text[index]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[open_index + 1 : index]
    raise AssertionError("unbalanced constructor")


def trial_prime(n: int, divisor: int, accumulated: bool) -> bool:
    assert divisor >= 2
    while divisor < n:
        if n % divisor == 0:
            accumulated = False
        divisor += 1
    return accumulated


def prime_nat(n: int) -> bool:
    return trial_prime(n, 2, n >= 2)


mpy_raw = Path("/tmp/audit-work/proof/solution.regenerated.mpy").read_text()
spec_raw = Path("/tmp/audit-work/proof/spec.k").read_text()

module_match = re.fullmatch(
    r'\s*Module\(\s*FuncDef\("prime_length",\s*Params\("string"\),'
    r"(?P<body>.*)\)\s*\)\s*",
    mpy_raw,
    re.DOTALL,
)
assert module_match, "regenerated module is not the required single binding/signature"

# The translator renders an omitted empty statement list as `,)`; the explicit
# `.Stmts` in the spec is the K unit for that same list sort.
translated_body = remove_k_whitespace(module_match.group("body")).replace(
    ",)", ",.Stmts)"
)
entry_start = spec_raw.index(
    '(Expr(Str("Return whether the length of string is a prime number."))',
    spec_raw.index("claim [prime-length]"),
) + 1
entry_end = spec_raw.index(".Stmts),", entry_start)
claimed_body = remove_k_whitespace(spec_raw[entry_start:entry_end])
assert translated_body == claimed_body

entry_text = remove_k_whitespace(
    spec_raw[spec_raw.index("claim [prime-length]") :]
)
assert '"prime_length"|->closureVal(("string",.ParamNames),' in entry_text
assert entry_text.count('"prime_length"|->closureVal') == 1
assert "),0),parent(-1))" in entry_text

translated_all = remove_k_whitespace(mpy_raw).replace(",)", ",.Stmts)")
spec_all = remove_k_whitespace(spec_raw)
translated_while_open = translated_all.index("While(") + len("While")
claimed_while_open = (
    spec_all.index("#while(", spec_all.index("claim[loop-invariant]"))
    + len("#while")
)
translated_while = balanced_contents(translated_all, translated_while_open)
claimed_while = balanced_contents(spec_all, claimed_while_open)
assert translated_while == claimed_while

canonical = load_entry("stage4_canonical", Path("/reference/canonical.py"))
candidate = load_entry("stage4_candidate", Path("/candidate/solution.py"))
substitutions = ["", "a", "ab", "abcd", "abcde"]
for value in substitutions:
    formal = prime_nat(len(value))
    trusted = canonical(value)
    generated = candidate(value)
    assert formal == trusted == generated
    print(
        f"entry substitution len={len(value)}: "
        f"primeNat={formal} canonical={trusted} candidate={generated}"
    )

loop_witness_result = trial_prime(4, 2, True)
assert loop_witness_result is False
print("loop precondition witness: N=4, D=2, P=true, S=str(.IntSeq)")
print("loop witness destination: trialPrime(4,2,true)=false")
print("entry precondition witness: CS=iCons(97,iCons(98,.IntSeq)), isLen(CS)=2")
print("binding/signature/body constructor comparison: MATCH")
print("loop condition/body constructor comparison: MATCH")
