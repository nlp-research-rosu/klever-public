#!/usr/bin/env python3
"""Mechanical constructor comparison and concrete claim-result substitutions."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from pathlib import Path


TOKEN = re.compile(
    r'"(?:\\.|[^"\\])*"'
    r"|#[A-Za-z][A-Za-z0-9]*"
    r"|\.[A-Za-z][A-Za-z0-9]*"
    r"|[A-Za-z][A-Za-z0-9]*"
    r"|-?[0-9]+"
    r"|[(),]"
)


def extract_module(text: str, anchor: str) -> str:
    anchor_pos = text.index(anchor)
    module_pos = text.index("Module", anchor_pos)
    open_pos = text.index("(", module_pos)
    depth = 0
    in_string = False
    escaped = False
    for pos in range(open_pos, len(text)):
        char = text[pos]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[module_pos:pos + 1]
    raise ValueError("unbalanced Module constructor")


def normalized_constructor_tokens(term: str) -> list[str]:
    # The translator omits explicit units for the Stmts list syntax. The spec
    # writes those same associative-list units as `.Stmts`.
    return [token for token in TOKEN.findall(term) if token != ".Stmts"]


def load_digits(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.digits


def odd_digits_product(value: int) -> int:
    if value <= 0:
        return 1
    digit = value % 10
    prefix = (value - digit) // 10
    if value % 2 == 1:
        return digit * odd_digits_product(prefix)
    return odd_digits_product(prefix)


def odd_digit_seen(value: int) -> int:
    if value <= 0:
        return 0
    prefix = (value - value % 10) // 10
    if value % 2 == 1:
        return 1
    return odd_digit_seen(prefix)


solution_text = Path(
    "/tmp/audit-work/source/regenerated-solution.mpy"
).read_text(encoding="utf-8")
spec_text = Path("/tmp/audit-work/source/spec.k").read_text(encoding="utf-8")
solution_module = extract_module(solution_text, "Module")
claim_module = extract_module(spec_text, "#loadAll")
solution_tokens = normalized_constructor_tokens(solution_module)
claim_tokens = normalized_constructor_tokens(claim_module)
solution_encoding = json.dumps(solution_tokens, separators=(",", ":")).encode()
claim_encoding = json.dumps(claim_tokens, separators=(",", ":")).encode()
print(f"solution_constructor_tokens={len(solution_tokens)}")
print(f"claim_constructor_tokens={len(claim_tokens)}")
print(f"spec_explicit_Stmts_units={claim_module.count('.Stmts')}")
print(
    "solution_constructor_sha256="
    f"{hashlib.sha256(solution_encoding).hexdigest()}"
)
print(
    "claim_constructor_sha256="
    f"{hashlib.sha256(claim_encoding).hexdigest()}"
)
print(f"constructor_equal={solution_tokens == claim_tokens}")
if solution_tokens != claim_tokens:
    for index, pair in enumerate(zip(solution_tokens, claim_tokens)):
        if pair[0] != pair[1]:
            print(f"first_difference index={index} solution={pair[0]} claim={pair[1]}")
            break
    raise SystemExit(1)

canonical = load_digits("trusted_canonical_pin", Path("/reference/canonical.py"))
candidate = load_digits(
    "scratch_candidate_pin", Path("/tmp/audit-work/source/solution.py")
)
substitutions = [
    1,
    4,
    10,
    235,
    2468,
    97531,
    1000000000000000000000000000000000000035,
]
for value in substitutions:
    claimed = odd_digits_product(value) * odd_digit_seen(value)
    canonical_value = canonical(value)
    candidate_value = candidate(value)
    print(
        f"N={value} precondition_N_gt_0={value > 0} "
        f"claimed_summary={claimed} canonical={canonical_value} "
        f"candidate={candidate_value} "
        f"all_equal={claimed == canonical_value == candidate_value}"
    )
    if claimed != canonical_value or claimed != candidate_value:
        raise SystemExit(2)

print(
    "entry_satisfying_state=N=1,env=0,scopeLoc=1,heap=.Map,"
    "heapLoc=0,stack=.List,ret=noRet,exc=NoExc,exitCode=0"
)
print(
    "loop_satisfying_state=N=0,P=7,F=0,L=1,PAR=parent(0),"
    "locals={n:0,product:7,found:0}"
)
