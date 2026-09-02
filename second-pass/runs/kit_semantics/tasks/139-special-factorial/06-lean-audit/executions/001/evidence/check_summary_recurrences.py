#!/usr/bin/env python3
"""Independent executable checks of the four Stage 1 summary equations."""

from __future__ import annotations

import json
import math


def source_loop(n: int, *, i: int = 1, factorial: int = 1, result: int = 1):
    while i <= n:
        factorial = factorial * i
        result = result * factorial
        i = i + 1
    return {"i": i, "factorial": factorial, "result": result}


def factorial_after(i: int, n: int, factorial: int) -> int:
    while i <= n:
        factorial = factorial * i
        i = i + 1
    return factorial


def product_after(i: int, n: int, factorial: int, result: int) -> int:
    while i <= n:
        factorial = factorial * i
        result = result * factorial
        i = i + 1
    return result


def human_contract(n: int) -> int:
    return math.prod(math.factorial(k) for k in range(1, n + 1))


def wrong_old_factorial(i: int, n: int, factorial: int, result: int) -> int:
    while i <= n:
        result = result * factorial
        factorial = factorial * i
        i = i + 1
    return result


cases = []
for n in range(1, 9):
    source = source_loop(n)
    cases.append(
        {
            "input": {"i": 1, "n": n, "factorial": 1, "result": 1},
            "source_final_state": source,
            "factorialAfter": factorial_after(1, n, 1),
            "productAfter": product_after(1, n, 1, 1),
            "human_contract": human_contract(n),
            "all_equal": (
                source["factorial"] == factorial_after(1, n, 1)
                and source["result"] == product_after(1, n, 1, 1)
                and source["result"] == human_contract(n)
            ),
        }
    )

adversarial_states = []
for i, n, factorial, result in [
    (5, 4, 7, 11),
    (4, 4, -3, 5),
    (2, 4, 7, 11),
    (-2, 1, 3, -5),
]:
    source = source_loop(n, i=i, factorial=factorial, result=result)
    adversarial_states.append(
        {
            "input": {"i": i, "n": n, "factorial": factorial, "result": result},
            "source_final_state": source,
            "factorialAfter": factorial_after(i, n, factorial),
            "productAfter": product_after(i, n, factorial, result),
            "matches_source": (
                source["factorial"] == factorial_after(i, n, factorial)
                and source["result"] == product_after(i, n, factorial, result)
            ),
        }
    )

counterfactual = {
    "input": {"i": 1, "n": 4, "factorial": 1, "result": 1},
    "correct_productAfter": product_after(1, 4, 1, 1),
    "identity_mutation": 1,
    "constant_zero_mutation": 0,
    "old_factorial_update_mutation": wrong_old_factorial(1, 4, 1, 1),
}

report = {
    "contract_cases": cases,
    "adversarial_summary_states": adversarial_states,
    "counterfactual_mutations": counterfactual,
    "contract_all_pass": all(case["all_equal"] for case in cases),
    "adversarial_all_pass": all(case["matches_source"] for case in adversarial_states),
    "counterfactuals_rejected": all(
        value != counterfactual["correct_productAfter"]
        for key, value in counterfactual.items()
        if key not in {"input", "correct_productAfter"}
    ),
}
print(json.dumps(report, indent=2, sort_keys=True))
raise SystemExit(
    0
    if report["contract_all_pass"]
    and report["adversarial_all_pass"]
    and report["counterfactuals_rejected"]
    else 1
)
