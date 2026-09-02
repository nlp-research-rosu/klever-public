#!/usr/bin/env python3
"""Mechanically compare solution.mpy with the claim's expanded program term."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


WORK = Path("/tmp/audit-work/run-002")
DEFINITION = WORK / "audit-verification-kompiled"


def parse_zero_arg_rule_bodies(text: str) -> dict[str, str]:
    lines = text.splitlines()
    result: dict[str, str] = {}
    index = 0
    start_re = re.compile(r"^\s*rule\s+([A-Za-z][A-Za-z0-9]*)\(\)\s*$")
    outer_re = re.compile(
        r"^\s*(?:syntax|rule|configuration|context|claim|alias|endmodule)\b"
    )
    while index < len(lines):
        match = start_re.match(lines[index])
        if not match:
            index += 1
            continue
        name = match.group(1)
        index += 1
        body_lines: list[str] = []
        while index < len(lines) and not outer_re.match(lines[index]):
            body_lines.append(lines[index])
            index += 1
        joined = "\n".join(body_lines).strip()
        if not joined.startswith("=>"):
            raise AssertionError(f"rule {name} does not begin with =>")
        result[name] = joined[2:].strip()
    return result


def expand_zero_arg_calls(term: str, rules: dict[str, str]) -> str:
    changed = True
    while changed:
        changed = False
        for name, body in rules.items():
            pattern = re.compile(rf"\b{re.escape(name)}\(\)")
            # Each helper has a declared result sort, so its RHS can replace
            # the call directly. K surface syntax does not provide arbitrary
            # grouping parentheses around list elements.
            replaced, count = pattern.subn(body, term)
            if count:
                term = replaced
                changed = True
    unresolved = sorted(set(re.findall(r"\b(allPrefixes(?:LoopBody|Body|Def)|solutionModule)\(\)", term)))
    if unresolved:
        raise AssertionError(f"unresolved constructor helpers: {unresolved}")
    return term


def kast_file(path: Path) -> dict[str, object]:
    command = [
        "kast",
        str(path),
        "--definition",
        str(DEFINITION),
        "--module",
        "MPY-SYNTAX",
        "--sort",
        "Module",
        "--output",
        "json",
    ]
    return json.loads(subprocess.check_output(command, cwd=WORK, text=True))["term"]


def kast_expression(expression: str) -> dict[str, object]:
    command = [
        "kast",
        "--expression",
        expression,
        "--definition",
        str(DEFINITION),
        "--module",
        "MPY-SYNTAX",
        "--sort",
        "Module",
        "--output",
        "json",
    ]
    return json.loads(subprocess.check_output(command, cwd=WORK, text=True))["term"]


def count_nodes(term: object) -> int:
    if isinstance(term, dict):
        return 1 + sum(count_nodes(value) for value in term.values())
    if isinstance(term, list):
        return sum(count_nodes(value) for value in term)
    return 0


def main() -> int:
    submitted = WORK / "solution.mpy"
    regenerated = WORK / "regenerated-solution.mpy"
    verification = (WORK / "verification.k").read_text(encoding="utf-8")
    rules = parse_zero_arg_rule_bodies(verification)
    required = {
        "allPrefixesLoopBody",
        "allPrefixesBody",
        "allPrefixesDef",
        "solutionModule",
    }
    if set(rules) != required:
        raise AssertionError(f"unexpected zero-argument rule inventory: {sorted(rules)}")

    expanded = expand_zero_arg_calls("solutionModule()", rules)
    # Rule bodies use explicit empty-list units because they are K sentences.
    # The .mpy program parser uses list sugar and spells those units by
    # omission, so render the expanded ground term in that equivalent form.
    expanded = expanded.replace("ListExpr(.Exprs)", "ListExpr()")
    expanded = expanded.replace(".Exprs", "")
    expanded = expanded.replace(".ParamNames", "")
    expanded = expanded.replace(".Stmts", "")
    source_term = kast_file(submitted)
    expanded_term = kast_expression(expanded)
    regenerated_identical = submitted.read_bytes() == regenerated.read_bytes()
    constructor_identical = source_term == expanded_term

    print(f"zero_arg_definition_rules={sorted(rules)}")
    print(f"trusted_regeneration_byte_identical={regenerated_identical}")
    print(f"source_kast_node_count={count_nodes(source_term)}")
    print(f"expanded_kast_node_count={count_nodes(expanded_term)}")
    print(f"constructor_terms_identical={constructor_identical}")
    print("expanded_solutionModule_surface_term:")
    print(expanded)
    if not regenerated_identical or not constructor_identical:
        return 1
    print("PROGRAM_TERM_CHECK=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
