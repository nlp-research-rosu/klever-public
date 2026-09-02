#!/usr/bin/env python3
"""Independent, non-executing source inspection and finite semantic checks."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


WORKSPACE = Path("/reference/k-proof")


def normalized(text: str) -> str:
    return " ".join(text.split())


def program(x: int, y: int) -> int:
    """Independent evaluator for the frozen conditional expression."""

    if x > y:
        return -1
    if y % 2 == 0:
        return y
    if x == y:
        return -1
    return y - 1


def source_oracle(x: int, y: int) -> int:
    evens = [value for value in range(x, y + 1) if value % 2 == 0]
    return max(evens) if evens else -1


def no_even_in_range(x: int, y: int) -> bool:
    return x > y or (x == y and x % 2 != 0)


def no_even_oracle(x: int, y: int) -> bool:
    return not any(value % 2 == 0 for value in range(x, y + 1))


def contract(x: int, y: int, result: int) -> bool:
    return (
        result == -1
        and no_even_in_range(x, y)
    ) or (
        result != -1
        and x <= result
        and result <= y
        and result % 2 == 0
        and y < result + 2
    )


def main() -> None:
    source_text = (WORKSPACE / "solution.py").read_text()
    source_tree = ast.parse(source_text)
    print("solution_ast", ast.dump(source_tree, indent=2))
    assert len(source_tree.body) == 1
    function = source_tree.body[0]
    assert isinstance(function, ast.FunctionDef)
    assert function.name == "choose_num"
    assert [argument.arg for argument in function.args.args] == ["x", "y"]
    assert len(function.body) == 1
    assert isinstance(function.body[0], ast.Return)

    inventory = inventory_verification(WORKSPACE)
    program_rule = inventory["rules"][0]["text"]
    program_rhs = program_rule.split("=>", 1)[1].strip()
    frozen_translation = (WORKSPACE / "solution.mpy").read_text().strip()
    print("program_term_normalized_equal", normalized(program_rhs) == normalized(frozen_translation))
    print(
        "program_term_sha256",
        hashlib.sha256(normalized(program_rhs).encode()).hexdigest(),
    )
    print(
        "solution_mpy_term_sha256",
        hashlib.sha256(normalized(frozen_translation).encode()).hexdigest(),
    )
    assert normalized(program_rhs) == normalized(frozen_translation)

    mismatches: list[dict[str, object]] = []
    for x in range(-50, 51):
        for y in range(-50, 51):
            observed = program(x, y)
            expected = source_oracle(x, y)
            if observed != expected:
                mismatches.append(
                    {
                        "kind": "program_oracle",
                        "x": x,
                        "y": y,
                        "observed": observed,
                        "expected": expected,
                    }
                )
            if no_even_in_range(x, y) != no_even_oracle(x, y):
                mismatches.append(
                    {
                        "kind": "no_even_summary",
                        "x": x,
                        "y": y,
                    }
                )
            if not contract(x, y, observed):
                mismatches.append(
                    {
                        "kind": "contract_rejects_program",
                        "x": x,
                        "y": y,
                        "result": observed,
                    }
                )
    print("tested_pairs", 101 * 101)
    print("mismatch_count", len(mismatches))
    if mismatches:
        print("first_mismatches", json.dumps(mismatches[:10], sort_keys=True))
    assert not mismatches

    witnesses = [
        (12, 15),
        (13, 12),
        (13, 13),
        (12, 12),
        (1, 1),
        (1, 2),
        (-3, -1),
    ]
    for x, y in witnesses:
        result = program(x, y)
        print(
            "witness",
            json.dumps(
                {
                    "x": x,
                    "y": y,
                    "result": result,
                    "no_even": no_even_in_range(x, y),
                    "contract": contract(x, y, result),
                },
                sort_keys=True,
            ),
        )

    adversarial = [
        {
            "name": "sentinel_when_even_exists",
            "x": 1,
            "y": 4,
            "result": -1,
        },
        {
            "name": "nonmaximal_even",
            "x": 1,
            "y": 4,
            "result": 2,
        },
        {
            "name": "odd_in_range",
            "x": 1,
            "y": 4,
            "result": 3,
        },
        {
            "name": "out_of_range_even",
            "x": 3,
            "y": 4,
            "result": 2,
        },
    ]
    for case in adversarial:
        accepted = contract(case["x"], case["y"], case["result"])
        print(
            "adversarial_contract",
            json.dumps({**case, "accepted": accepted}, sort_keys=True),
        )
        assert not accepted

    # Counterfactual mutations demonstrate that the equations constrain the
    # intended edge cases rather than collapsing to convenient constants.
    mutated_no_even = lambda x, y: x > y
    print(
        "counterfactual_drop_odd_singleton",
        {
            "x": 13,
            "y": 13,
            "actual": no_even_in_range(13, 13),
            "mutated": mutated_no_even(13, 13),
        },
    )
    assert no_even_in_range(13, 13) and not mutated_no_even(13, 13)

    mutated_odd_branch = lambda x, y: (
        -1 if x > y else (y if y % 2 == 0 else (-1 if x == y else y - 3))
    )
    print(
        "counterfactual_y_minus_3",
        {
            "x": 1,
            "y": 5,
            "actual": program(1, 5),
            "mutated": mutated_odd_branch(1, 5),
            "oracle": source_oracle(1, 5),
        },
    )
    assert mutated_odd_branch(1, 5) != source_oracle(1, 5)

    print("semantic_checks", "PASS")


if __name__ == "__main__":
    main()
