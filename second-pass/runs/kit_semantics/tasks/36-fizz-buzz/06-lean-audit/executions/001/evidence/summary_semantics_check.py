#!/usr/bin/env python3
"""Independent executable checks for the six Stage 3 recurrence equations."""

from __future__ import annotations

import random


def digit_result(count: int, value: int) -> int:
    while value > 0:
        count += int(value % 10 == 7)
        value //= 10
    return count


def fizz_result(count: int, bound: int) -> int:
    while bound > 0:
        bound -= 1
        if bound % 11 == 0 or bound % 13 == 0:
            count = digit_result(count, bound)
    return count


def source_program(bound: int) -> int:
    count = 0
    candidate = bound
    value = 0
    while candidate > 0:
        candidate -= 1
        if candidate % 11 == 0 or candidate % 13 == 0:
            value = candidate
            while value > 0:
                count += int(value % 10 == 7)
                value //= 10
    return count


def mutant_digit_eight(bound: int) -> int:
    return sum(
        str(candidate).count("8")
        for candidate in range(max(bound, 0))
        if candidate % 11 == 0 or candidate % 13 == 0
    )


def mutant_and(bound: int) -> int:
    return sum(
        str(candidate).count("7")
        for candidate in range(max(bound, 0))
        if candidate % 11 == 0 and candidate % 13 == 0
    )


def mutant_process_bound_first(bound: int) -> int:
    return sum(
        str(candidate).count("7")
        for candidate in range(1, max(bound, 0) + 1)
        if candidate % 11 == 0 or candidate % 13 == 0
    )


def main() -> None:
    # Exhaustive operational-to-summary comparison over negative and positive bounds.
    checked = list(range(-50, 1001))
    mismatches = [
        (bound, source_program(bound), fizz_result(0, bound))
        for bound in checked
        if source_program(bound) != fizz_result(0, bound)
    ]
    print(f"operational_summary.bounds={checked[0]}..{checked[-1]}")
    print(f"operational_summary.mismatches={len(mismatches)}")

    # Each equation is checked for varied accumulators and positive/terminal bounds.
    rng = random.Random(3607)
    accumulators = [-17, -1, 0, 1, 23] + [rng.randint(-100, 100) for _ in range(20)]
    digit_base_failures = 0
    digit_terminal_failures = 0
    digit_step_failures = 0
    fizz_base_failures = 0
    fizz_qualifying_failures = 0
    fizz_nonqualifying_failures = 0
    for count in accumulators:
        for value in range(-20, 501):
            if value <= 0:
                digit_base_failures += digit_result(count, value) != count
                fizz_base_failures += fizz_result(count, value) != count
            else:
                quotient, remainder = divmod(value, 10)
                if quotient <= 0:
                    digit_terminal_failures += (
                        digit_result(count, value)
                        != count + int(remainder == 7)
                    )
                digit_step_failures += (
                    digit_result(count + int(remainder == 7), quotient)
                    != digit_result(count, value)
                )

                candidate = value - 1
                qualifying = candidate % 11 == 0 or candidate % 13 == 0
                if qualifying:
                    fizz_qualifying_failures += (
                        fizz_result(digit_result(count, candidate), candidate)
                        != fizz_result(count, value)
                    )
                else:
                    fizz_nonqualifying_failures += (
                        fizz_result(count, candidate)
                        != fizz_result(count, value)
                    )
    print(f"digit.base.failures={digit_base_failures}")
    print(f"digit.terminal.failures={digit_terminal_failures}")
    print(f"digit.step.failures={digit_step_failures}")
    print(f"fizz.base.failures={fizz_base_failures}")
    print(f"fizz.qualifying.failures={fizz_qualifying_failures}")
    print(f"fizz.nonqualifying.failures={fizz_nonqualifying_failures}")

    # The supplied examples and counterfactual witnesses establish relevance.
    for bound in (50, 78, 79):
        print(f"source.example[{bound}]={source_program(bound)}")
    witness = 78
    expected = source_program(witness)
    print(f"counterfactual.bound={witness}")
    print(f"counterfactual.expected={expected}")
    print(f"counterfactual.constant_zero={0}")
    print(f"counterfactual.identity_summary={0}")
    print(f"counterfactual.digit_eight={mutant_digit_eight(witness)}")
    print(f"counterfactual.and_instead_of_or={mutant_and(witness)}")
    print(f"counterfactual.process_bound_first={mutant_process_bound_first(witness)}")

    failures = (
        len(mismatches)
        + digit_base_failures
        + digit_terminal_failures
        + digit_step_failures
        + fizz_base_failures
        + fizz_qualifying_failures
        + fizz_nonqualifying_failures
    )
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
