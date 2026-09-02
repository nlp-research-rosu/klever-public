#!/usr/bin/env python3
"""Check the implementation and proof prime tables against trial division."""

from __future__ import annotations

import ast
import re
from pathlib import Path


SOLUTION = Path("/tmp/audit-work/clean/candidate/solution.py")
VERIFICATION = Path("/tmp/audit-work/clean/candidate/verification.k")


def primes_through(limit: int) -> list[int]:
    result = []
    for value in range(2, limit + 1):
        if all(value % divisor for divisor in range(2, int(value**0.5) + 1)):
            result.append(value)
    return result


def python_list() -> list[int]:
    tree = ast.parse(SOLUTION.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare) and isinstance(node.comparators[0], ast.List):
            return [ast.literal_eval(item) for item in node.comparators[0].elts]
    raise RuntimeError("prime membership list not found")


def k_rule_list(text: str, start: str, end: str) -> list[int]:
    section = text.split(start, 1)[1].split(end, 1)[0]
    return [int(value) for value in re.findall(r"Int\((\d+)\)", section)]


def main() -> int:
    verification = VERIFICATION.read_text()
    expected = primes_through(100)
    source = python_list()
    solution_k = k_rule_list(
        verification, "rule solutionPrimes =>", 'syntax Stmts ::= "solutionLoopBody"'
    )
    contract_k = k_rule_list(
        verification, "rule contractPrimes =>", 'syntax Bool ::= "primeLength"'
    )
    print(f"trial_division_primes_2_through_100={expected}")
    print(f"solution_python_list={source}")
    print(f"solutionPrimes={solution_k}")
    print(f"contractPrimes={contract_k}")
    print(f"source_matches_math={source == expected}")
    print(f"solution_k_matches_source={solution_k == source}")
    print(f"contract_k_matches_math={contract_k == expected}")
    return 0 if source == solution_k == contract_k == expected else 1


if __name__ == "__main__":
    raise SystemExit(main())
