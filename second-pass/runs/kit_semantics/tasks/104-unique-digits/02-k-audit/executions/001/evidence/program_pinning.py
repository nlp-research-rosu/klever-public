#!/usr/bin/env python3
"""Mechanically compare the submitted MPY function with the entry-claim term."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


SOLUTION = Path("/tmp/audit-work/candidate-src/solution.mpy")
SPEC = Path("/tmp/audit-work/candidate-src/spec.k")
DEFINITION = Path("/tmp/audit-work/candidate-src/verification-audit-kompiled")


def balanced_call(text: str, start: int) -> str:
    open_index = text.index("(", start)
    depth = 0
    quote = False
    escaped = False
    for index in range(open_index, len(text)):
        char = text[index]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quote = False
            continue
        if char == '"':
            quote = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise AssertionError(f"unbalanced term starting at offset {start}")


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


solution_text = SOLUTION.read_text(encoding="utf-8")
solution_start = solution_text.index("FuncDef(")
solution_func = balanced_call(solution_text, solution_start)
assert compact(solution_text) == f"Module({compact(solution_func)})"

spec_text = SPEC.read_text(encoding="utf-8")
program_claim = spec_text[spec_text.index("claim [program]:") :]
claim_start = program_claim.index("FuncDef(")
claim_func = balanced_call(program_claim, claim_start)
assert program_claim.index("~> Call(") > claim_start + len(claim_func)


def parse_surface_expanded(term: str) -> dict[str, object]:
    command = [
        "kast",
        "--definition",
        str(DEFINITION),
        "--module",
        "MPY-SYNTAX",
        "--sort",
        "Stmt",
        "--expand-macros",
        "--output",
        "json",
        "--expression",
        term,
    ]
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    print("KAST_COMMAND:", " ".join(command[:-1]), "<TERM>")
    print("KAST_EXIT_STATUS:", result.returncode)
    if result.stderr:
        print("KAST_STDERR:", result.stderr.strip())
    assert result.returncode == 0
    return json.loads(result.stdout)["term"]


def parse_claim_expanded(term: str) -> dict[str, object]:
    command = [
        "kast",
        "--definition",
        str(DEFINITION),
        "--module",
        "VERIFICATION",
        "--input",
        "rule",
        "--expand-macros",
        "--output",
        "json",
        "--expression",
        f"{term} => {term}",
    ]
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    print("KAST_COMMAND:", " ".join(command[:-1]), "<TERM => TERM>")
    print("KAST_EXIT_STATUS:", result.returncode)
    if result.stderr:
        print("KAST_STDERR:", result.stderr.strip())
    assert result.returncode == 0
    parsed = json.loads(result.stdout)["term"]
    assert parsed["node"] == "KRewrite"
    assert parsed["lhs"] == parsed["rhs"]
    return parsed["lhs"]


solution_kast = parse_surface_expanded(solution_func)
claim_kast = parse_claim_expanded(claim_func)
solution_canonical = json.dumps(
    solution_kast, sort_keys=True, separators=(",", ":")
).encode()
claim_canonical = json.dumps(
    claim_kast, sort_keys=True, separators=(",", ":")
).encode()
print("solution-expanded-kast-sha256:", hashlib.sha256(solution_canonical).hexdigest())
print("claim-expanded-kast-sha256:", hashlib.sha256(claim_canonical).hexdigest())
print("expanded-kast-byte-equal:", solution_canonical == claim_canonical)
assert solution_canonical == claim_canonical


def find_single_kapply(
    term: dict[str, object], label_prefix: str
) -> dict[str, object]:
    matches: list[dict[str, object]] = []

    def visit(node: object) -> None:
        if isinstance(node, dict):
            if node.get("node") == "KApply":
                label = node["label"]
                assert isinstance(label, dict)
                name = label["name"]
                assert isinstance(name, str)
                if name.startswith(label_prefix):
                    matches.append(node)
            for value in node.values():
                visit(value)
        elif isinstance(node, list):
            for value in node:
                visit(value)

    visit(term)
    assert len(matches) == 1, (label_prefix, len(matches))
    return matches[0]


digit_start = spec_text.index("#while(")
digit_term = balanced_call(spec_text, digit_start)
outer_start = spec_text.index("#loop(", digit_start + len(digit_term))
outer_term = balanced_call(spec_text, outer_start)
digit_kast = parse_claim_expanded(digit_term)
outer_kast = parse_claim_expanded(outer_term)
solution_while = find_single_kapply(solution_kast, "While(_,_)")
solution_for = find_single_kapply(solution_kast, "For(_,_,_)")

assert solution_while["args"] == digit_kast["args"]
assert solution_for["args"][0] == outer_kast["args"][1]
assert solution_for["args"][2] == outer_kast["args"][2]
print("digit-loop-condition-and-body-equal:", True)
print("outer-loop-target-and-body-equal:", True)
print("PROGRAM_PINNING_CHECK: PASS")
