#!/usr/bin/env python3
"""Exhibit a satisfying witness and result check for every submitted entry claim."""

from __future__ import annotations

import importlib.util
import itertools
import re
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.strange_sort_list


def split_top_level(text: str) -> tuple[str, str]:
    depth = 0
    for index, char in enumerate(text):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 1:
            return text[5:index], text[index + 1 : -1]
    raise AssertionError(text)


def parse_plist(term: str, bindings: dict[str, int]) -> list[int]:
    compact = re.sub(r"\s+", "", term)
    if compact == "nil":
        return []
    assert compact.startswith("cons(") and compact.endswith(")"), compact
    head, tail = split_top_level(compact)
    head = re.sub(r":Int$", "", head)
    value = bindings[head] if head in bindings else int(head)
    return [value, *parse_plist(tail, bindings)]


def satisfies(condition: str, bindings: dict[str, int]) -> bool:
    if not condition:
        return True
    clauses = re.split(r"\s+andBool\s+", condition)
    for clause in clauses:
        match = re.fullmatch(r"\s*([A-D])\s*(<=Int|>Int)\s*([A-D])\s*", clause)
        assert match is not None, clause
        left, operator, right = match.groups()
        if operator == "<=Int" and not bindings[left] <= bindings[right]:
            return False
        if operator == ">Int" and not bindings[left] > bindings[right]:
            return False
    return True


def weave(values: list[int]) -> list[int]:
    ordered = sorted(values)
    result: list[int] = []
    while ordered:
        result.append(ordered.pop(0))
        if ordered:
            result.append(ordered.pop())
    return result


spec_text = Path("/candidate/spec.k").read_text()
chunks = re.split(r"(?m)^\s*claim\s*$", spec_text)[1:]
assert len(chunks) == 39
canonical = load_function(Path("/reference/canonical.py"), "witness_canonical")
candidate = load_function(Path("/candidate/solution.py"), "witness_candidate")

length_counts: dict[int, int] = {}
for claim_number, chunk in enumerate(chunks, 1):
    input_match = re.search(r"<input>\s*(.*?)\s*</input>", chunk, re.S)
    result_match = re.search(
        r"<result>\s*pending\s*=>\s*pList\((.*?)\)\s*</result>", chunk, re.S
    )
    requires_match = re.search(r"(?m)^\s*requires\s+(.*?)\s*$", chunk)
    assert input_match is not None and result_match is not None
    input_term = input_match.group(1)
    result_term = result_match.group(1)
    condition = requires_match.group(1) if requires_match else ""
    variables = sorted(set(re.findall(r"\b([A-D])(?::Int)?\b", input_term)))

    witness_bindings: dict[str, int] | None = None
    for values in itertools.product(range(-3, 4), repeat=len(variables)):
        trial = dict(zip(variables, values))
        if satisfies(condition, trial):
            witness_bindings = trial
            break
    assert witness_bindings is not None
    input_values = parse_plist(input_term, witness_bindings)

    if "strangeSpec" in result_term:
        expected = weave(input_values)
    else:
        expected = parse_plist(result_term, witness_bindings)
    canonical_result = canonical(list(input_values))
    candidate_result = candidate(list(input_values))
    assert expected == canonical_result == candidate_result
    length_counts[len(input_values)] = length_counts.get(len(input_values), 0) + 1
    printable_pre = condition or "true"
    print(
        f"claim={claim_number:02d} pre={printable_pre} "
        f"bindings={witness_bindings} input={input_values} result={expected}"
    )

print(f"claim_count={len(chunks)}")
print(f"claim_witness_length_counts={dict(sorted(length_counts.items()))}")
print("ALL CLAIM PRECONDITIONS SATISFIABLE; ALL WITNESS RESULTS AGREE")
