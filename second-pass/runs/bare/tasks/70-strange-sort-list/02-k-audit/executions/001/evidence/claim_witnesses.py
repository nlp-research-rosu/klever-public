#!/usr/bin/env python3
"""Find and check one concrete satisfying state for every submitted claim."""

from __future__ import annotations

import importlib.util
import itertools
import re
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_plist(term: str, env: dict[str, int]) -> list[int]:
    tokens = re.findall(r"cons|nil|-?\d+|[A-Z]|[(),]", term.replace(":Int", ""))
    pos = 0

    def take(expected: str | None = None) -> str:
        nonlocal pos
        if pos >= len(tokens):
            raise ValueError(f"unexpected end parsing {term!r}")
        token = tokens[pos]
        pos += 1
        if expected is not None and token != expected:
            raise ValueError(f"expected {expected!r}, got {token!r}")
        return token

    def parse_list() -> list[int]:
        token = take()
        if token == "nil":
            return []
        if token != "cons":
            raise ValueError(f"expected list constructor, got {token!r}")
        take("(")
        head_token = take()
        head = env[head_token] if head_token in env else int(head_token)
        take(",")
        tail = parse_list()
        take(")")
        return [head, *tail]

    result = parse_list()
    if pos != len(tokens):
        raise ValueError(f"unconsumed tokens in {term!r}: {tokens[pos:]}")
    return result


def holds(precondition: str, env: dict[str, int]) -> bool:
    if precondition == "<none>":
        return True
    expression = precondition.replace("<=Int", "<=")
    expression = expression.replace(">Int", ">")
    expression = expression.replace("andBool", "and")
    return bool(eval(expression, {"__builtins__": {}}, env))


def contract(values: list[int]) -> list[int]:
    remaining = values.copy()
    result: list[int] = []
    choose_minimum = True
    while remaining:
        selected = min(remaining) if choose_minimum else max(remaining)
        result.append(selected)
        remaining.remove(selected)
        choose_minimum = not choose_minimum
    return result


def main() -> int:
    text = Path("/tmp/audit-work/src/spec.k").read_text()
    blocks = re.findall(
        r"(?ms)^  claim\s*$\n(.*?)(?=^  claim\s*$|^endmodule\s*$)", text
    )
    canonical = load_module("trusted_canonical", Path("/reference/canonical.py"))
    candidate = load_module(
        "scratch_candidate", Path("/tmp/audit-work/src/solution.py")
    )
    failures = 0
    symbolic_partitions: dict[int, list[str]] = {2: [], 3: [], 4: []}

    for claim_index, block in enumerate(blocks, 1):
        input_match = re.search(r"<input>\s*(.*?)\s*</input>", block)
        result_match = re.search(
            r"<result>\s*pending\s*=>\s*(.*?)\s*</result>", block
        )
        requires_match = re.search(r"(?m)^\s+requires\s+(.+)$", block)
        if input_match is None or result_match is None:
            raise ValueError(f"claim {claim_index}: missing input or result")
        input_term = input_match.group(1)
        result_term = result_match.group(1)
        precondition = requires_match.group(1) if requires_match else "<none>"
        variables = sorted(set(re.findall(r"\b([A-Z]):Int\b", input_term)))
        if (
            len(variables) in symbolic_partitions
            and "strangeSpec(" in result_term
        ):
            symbolic_partitions[len(variables)].append(precondition)

        witness_env: dict[str, int] | None = None
        for values in itertools.product(range(-3, 4), repeat=len(variables)):
            possible = dict(zip(variables, values))
            if holds(precondition, possible):
                witness_env = possible
                break
        if witness_env is None:
            print(f"CLAIM={claim_index} SAT=false PRECONDITION={precondition}")
            failures += 1
            continue

        witness_input = parse_plist(input_term, witness_env)
        natural_result = contract(witness_input)
        if "strangeSpec(" in result_term:
            interpreted_claim_result = natural_result
        else:
            plist_match = re.fullmatch(r"pList\((.*)\)", result_term)
            if plist_match is None:
                raise ValueError(
                    f"claim {claim_index}: unrecognized result {result_term!r}"
                )
            interpreted_claim_result = parse_plist(
                plist_match.group(1), witness_env
            )
        canonical_result = canonical.strange_sort_list(witness_input.copy())
        candidate_result = candidate.strange_sort_list(witness_input.copy())
        matched = (
            interpreted_claim_result
            == natural_result
            == canonical_result
            == candidate_result
        )
        failures += not matched
        print(f"CLAIM={claim_index}")
        print(f"PRECONDITION={precondition}")
        print(f"WITNESS_ENV={witness_env}")
        print(f"WITNESS_INPUT={witness_input}")
        print(f"CLAIM_RESULT={interpreted_claim_result}")
        print(f"NATURAL_CONTRACT={natural_result}")
        print(f"PYTHON_CANONICAL={canonical_result}")
        print(f"PYTHON_CANDIDATE={candidate_result}")
        print(f"MATCH={str(matched).lower()}")

    for length, preconditions in symbolic_partitions.items():
        uncovered = 0
        overlaps = 0
        assignments = 0
        variable_names = [chr(ord("A") + offset) for offset in range(length)]
        for values in itertools.product(range(-3, 4), repeat=length):
            env = dict(zip(variable_names, values))
            matches = sum(holds(precondition, env) for precondition in preconditions)
            assignments += 1
            uncovered += matches == 0
            overlaps += matches > 1
        print(f"PARTITION_LENGTH={length}")
        print(f"PARTITION_CLAIMS={len(preconditions)}")
        print(f"PARTITION_ASSIGNMENTS={assignments}")
        print(f"PARTITION_UNCOVERED={uncovered}")
        print(f"PARTITION_OVERLAPS={overlaps}")
        failures += uncovered + overlaps

    print(f"CLAIMS={len(blocks)}")
    print(f"FAILURES={failures}")
    print(f"RESULT={'PASS' if len(blocks) == 39 and failures == 0 else 'FAIL'}")
    return int(len(blocks) != 39 or failures != 0)


if __name__ == "__main__":
    raise SystemExit(main())
