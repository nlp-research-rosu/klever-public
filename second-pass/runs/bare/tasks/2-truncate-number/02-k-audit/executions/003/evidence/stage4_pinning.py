#!/usr/bin/env python3
"""Mechanical token-level pinning of each entry claim to solution.mpy."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path


TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|[A-Za-z][A-Za-z0-9_-]*|-?[0-9]+|[(),]')


def constructor_tokens(text: str, constructor: str) -> tuple[str, ...]:
    tokens = TOKEN.findall(text)
    start = tokens.index(constructor)
    assert tokens[start + 1] == "("
    depth = 0
    end = None
    for index in range(start + 1, len(tokens)):
        if tokens[index] == "(":
            depth += 1
        elif tokens[index] == ")":
            depth -= 1
            if depth == 0:
                end = index + 1
                break
    assert end is not None
    return tuple(tokens[start:end])


def all_constructor_tokens(text: str, constructor: str) -> list[tuple[str, ...]]:
    tokens = TOKEN.findall(text)
    terms: list[tuple[str, ...]] = []
    index = 0
    while index < len(tokens):
        if tokens[index] != constructor:
            index += 1
            continue
        assert tokens[index + 1] == "("
        depth = 0
        for end in range(index + 1, len(tokens)):
            if tokens[end] == "(":
                depth += 1
            elif tokens[end] == ")":
                depth -= 1
                if depth == 0:
                    terms.append(tuple(tokens[index : end + 1]))
                    index = end + 1
                    break
        else:
            raise AssertionError(f"unbalanced {constructor} term")
    return terms


mpy = Path("/tmp/audit-work/source/solution.mpy").read_text(encoding="utf-8")
spec = Path("/tmp/audit-work/source/spec.k").read_text(encoding="utf-8")
program = constructor_tokens(mpy, "Module")
claim_programs = all_constructor_tokens(spec, "Module")
print(f"solution_constructor_tokens={len(program)}")
print(f"entry_claim_program_terms={len(claim_programs)}")
for index, claim_program in enumerate(claim_programs, 1):
    identical = claim_program == program
    print(f"claim_{index}_constructor_identical={identical}")
    assert identical

semantic = Path("/tmp/audit-work/source/semantic.k").read_text(encoding="utf-8")
entry_shape = (
    'Module(FuncDef(F, Params(P), BODY)) ~> invoke(F, V) => BODY'
)
assert entry_shape in " ".join(semantic.split())
print("entry_rule_executes_matched_BODY=True")

# Satisfying witness for the symbolic claim: 3.5 = 3 + 5/10.
I, F, S = 3, 5, 10
valid_positive = (
    S > 0 and I >= 0 and F >= 0 and F < S and (I > 0 or F > 0)
)
valid_fraction = 0 == 0 and S > 0 and F >= 0 and F < S
print(
    f"witness=num({I},{F},{S}) "
    f"validPositive={valid_positive} result=num(0,{F},{S}) "
    f"validFraction={valid_fraction}"
)
assert valid_positive and valid_fraction


def load(path: Path, name: str):
    module_spec = importlib.util.spec_from_file_location(name, path)
    assert module_spec is not None and module_spec.loader is not None
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


canonical = load(Path("/reference/canonical.py"), "pinning_canonical")
candidate = load(Path("/tmp/audit-work/source/solution.py"), "pinning_candidate")
number = I + F / S
print(
    f"witness_python_input={number!r} canonical={canonical.truncate_number(number)!r} "
    f"candidate={candidate.truncate_number(number)!r} claimed_rational={F}/{S}"
)
assert canonical.truncate_number(number) == candidate.truncate_number(number) == F / S
print("STAGE4_PINNING_OK")
