#!/usr/bin/env python3
"""Mechanical constructor comparison and concrete precondition witnesses."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path
from typing import Callable


ROOT = Path("/tmp/audit-work/134-check-last-char")


def balanced_call(text: str, marker: str, start: int = 0) -> tuple[str, int]:
    marker_at = text.index(marker, start)
    open_at = marker_at + len(marker) - 1
    if text[open_at] != "(":
        raise ValueError(f"marker must end in opening parenthesis: {marker}")
    depth = 0
    quoted = False
    escaped = False
    for index in range(open_at, len(text)):
        char = text[index]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[open_at + 1 : index], index + 1
    raise ValueError(f"unterminated call: {marker}")


def top_level_args(content: str) -> list[str]:
    args: list[str] = []
    start = 0
    depth = 0
    quoted = False
    escaped = False
    for index, char in enumerate(content):
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            args.append(content[start:index].strip())
            start = index + 1
    args.append(content[start:].strip())
    return args


TOKEN = re.compile(
    r'"(?:\\.|[^"\\])*"|'
    r"\.[A-Za-z_][A-Za-z0-9_-]*|"
    r"[A-Za-z_][A-Za-z0-9_-]*|"
    r"-?[0-9]+|"
    r"==|!=|<=|>=|"
    r"[(),]|"
    r"\S"
)


def normalized_constructor_tokens(term: str) -> list[str]:
    tokens = [token for token in TOKEN.findall(term) if token not in {".Exprs", ".Stmts"}]
    changed = True
    while changed:
        changed = False
        new: list[str] = []
        for index, token in enumerate(tokens):
            if token == "," and index + 1 < len(tokens) and tokens[index + 1] == ")":
                changed = True
                continue
            new.append(token)
        tokens = new
    return tokens


def load_entry(path: Path, module_name: str) -> Callable[[str], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check_if_last_char_is_a_letter


solution_mpy = (ROOT / "solution.mpy").read_text()
regenerated_mpy = (ROOT / "solution.regenerated.mpy").read_text()
spec_text = (ROOT / "spec.k").read_text()

func_content, _func_end = balanced_call(solution_mpy, "FuncDef(")
func_args = top_level_args(func_content)
if len(func_args) != 3:
    raise RuntimeError(f"unexpected FuncDef arity: {len(func_args)}")
function_name, parameters, function_body = func_args

closures: list[list[str]] = []
position = 0
while True:
    try:
        closure_content, position = balanced_call(spec_text, "closureVal(", position)
    except ValueError:
        break
    closures.append(top_level_args(closure_content))

print(f"submitted_vs_regenerated_bytes_equal={solution_mpy == regenerated_mpy}")
print(f"function_name={function_name}")
print(f"parameters={parameters}")
print(f"closure_count={len(closures)}")
source_tokens = normalized_constructor_tokens(function_body)
print(f"normalized_source_body_token_count={len(source_tokens)}")

all_match = True
for index, closure_args in enumerate(closures, 1):
    if len(closure_args) != 4:
        raise RuntimeError(f"closure {index} has unexpected arity {len(closure_args)}")
    closure_param, cell_vars, closure_body, defining_env = closure_args
    closure_tokens = normalized_constructor_tokens(closure_body)
    match = (
        closure_param == '"txt"'
        and cell_vars == ".ParamNames"
        and defining_env == "0"
        and closure_tokens == source_tokens
    )
    all_match = all_match and match
    print(
        f"closure_{index} param={closure_param} cell_vars={cell_vars} "
        f"defining_env={defining_env} body_tokens={len(closure_tokens)} "
        f"constructor_body_match={match}"
    )
    if closure_tokens != source_tokens:
        for token_index, (left, right) in enumerate(
            zip(source_tokens, closure_tokens), 1
        ):
            if left != right:
                print(
                    f"FIRST_TOKEN_DIFF closure={index} token={token_index} "
                    f"source={left!r} claim={right!r}"
                )
                break

required_fragments = [
    "<env> 0 </env>",
    "<scopeLoc> 1 </scopeLoc>",
    "<heap> .Map </heap>",
    "<heapLoc> 0 </heapLoc>",
    "<stack> .List </stack>",
    "<ret> noRet </ret>",
    "<exc> NoExc </exc>",
    "<exit-code> 0 </exit-code>",
    '"check_if_last_char_is_a_letter" |->',
    "-1 |-> builtinsScope",
]
for fragment in required_fragments:
    count = spec_text.count(fragment)
    print(f"state_fragment={fragment!r} count={count}")
    all_match = all_match and count == 3

candidate = load_entry(ROOT / "solution.py", "audit_pinning_candidate")
canonical = load_entry(ROOT / "canonical.py", "audit_pinning_canonical")
witnesses = [
    ("target-empty", "", False),
    ("target-nonalpha", "1", False),
    ("target-alpha-singleton", "a", True),
    ("target-alpha-long-true", " a", True),
    ("target-alpha-long-false", "ba", False),
]
for claim, value, formal_result in witnesses:
    candidate_result = candidate(value)
    canonical_result = canonical(value)
    print(
        f"WITNESS claim={claim} input={value!r} formal={formal_result} "
        f"candidate={candidate_result} canonical={canonical_result}"
    )
    all_match = all_match and candidate_result == formal_result == canonical_result

print(f"PINNING_AND_WITNESS_CHECK={all_match}")
raise SystemExit(0 if all_match else 1)
