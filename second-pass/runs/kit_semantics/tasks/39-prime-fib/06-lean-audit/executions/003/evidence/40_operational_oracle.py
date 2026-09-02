#!/usr/bin/env python3
"""Independent finite oracle for the frozen prime-fib summaries."""

from __future__ import annotations


def py_mod(x: int, y: int) -> int:
    # Frozen K: ((x %Int y) +Int y) %Int y, where %Int is truncating.
    trunc = x - int(x / y) * y
    return (trunc + y) - int((trunc + y) / y) * y


def source_scan(a: int, d: int, flag: bool) -> bool:
    while d * d <= a:
        if py_mod(a, d) == 0:
            flag = False
        d += 1
    return flag


def candidate_scan_port(a: int, d: int, flag: bool) -> bool:
    if d < 2:
        return False
    if not flag:
        return False
    fuel = max(a, 0) + 1
    while fuel:
        if d * d > a:
            return True
        if py_mod(a, d) == 0:
            return False
        d += 1
        fuel -= 1
    return True  # Exact port of runPrimeDivisorScan's zero-fuel branch.


def increment(b: int) -> int:
    return int(source_scan(b, 2, b >= 2))


def step(state: tuple[int, int, int]) -> tuple[int, int, int]:
    count, a, b = state
    return count + increment(b), b, a + b


def source_search_bounded(
    target: int, state: tuple[int, int, int], limit: int = 500
) -> tuple[str, int | None, int]:
    for steps in range(limit + 1):
        count, a, _b = state
        if count >= target:
            return "reached", a, steps
        state = step(state)
    return "unresolved", None, limit


def candidate_search_port_bounded(
    target: int, state: tuple[int, int, int], limit: int = 500
) -> tuple[str, int | None]:
    count, a, b = state
    if target <= count:
        return "reached", a
    if target < 1 or b < 1:
        return "totalized", 0
    next_state = step(state)
    if target <= next_state[0]:
        return "reached", next_state[1]
    if a < 0:
        return "totalized", 0
    status, value, _steps = source_search_bounded(target, next_state, limit)
    return status, value


scan_cases = 0
scan_mismatches: list[tuple[object, ...]] = []
for a in range(-10, 201):
    for d in range(2, 31):
        for flag in (False, True):
            scan_cases += 1
            observed = candidate_scan_port(a, d, flag)
            expected = source_scan(a, d, flag)
            if observed != expected:
                scan_mismatches.append((a, d, flag, observed, expected))

definition_failures: list[tuple[object, ...]] = []
for a in range(-10, 201):
    for d in range(2, 31):
        for flag in (False, True):
            got = source_scan(a, d, flag)
            if d * d > a and got != flag:
                definition_failures.append(("scan-base", a, d, flag))
            if d * d <= a and py_mod(a, d) == 0 and got is not False:
                definition_failures.append(("scan-divisor", a, d, flag))
            if (
                d * d <= a
                and py_mod(a, d) != 0
                and source_scan(a, d + 1, flag) != got
            ):
                definition_failures.append(("scan-recurrence", a, d, flag))
            if source_scan(a, d, False) is not False:
                definition_failures.append(("false-absorption", a, d))

search_cases = 0
search_mismatches: list[tuple[object, ...]] = []
recurrence_cases = 0
recurrence_failures: list[tuple[object, ...]] = []
exit_cases = 0
exit_failures: list[tuple[object, ...]] = []
for target in range(1, 5):
    for count in range(0, target):
        for a in range(0, 7):
            for b in range(1, 16):
                state = (count, a, b)
                expected_status, expected, _ = source_search_bounded(
                    target, state, 25
                )
                candidate_status, observed = candidate_search_port_bounded(
                    target, state, 25
                )
                if expected_status == "reached":
                    search_cases += 1
                    if candidate_status != "reached" or observed != expected:
                        search_mismatches.append(
                            (target, state, candidate_status, observed, expected)
                        )
                    next_state = step(state)
                    next_status, next_value, _ = source_search_bounded(
                        target, next_state, 25
                    )
                    if next_status == "reached":
                        recurrence_cases += 1
                        if next_value != expected:
                            recurrence_failures.append(
                                (target, state, expected, next_value)
                            )
                next_count = count + increment(b)
                if not (next_count < target):
                    exit_cases += 1
                    status, value = candidate_search_port_bounded(
                        target, state, 25
                    )
                    if status != "reached" or value != b:
                        exit_failures.append((target, state, status, value))

initial_values = []
for target in range(1, 11):
    source_status, source_value, steps = source_search_bounded(
        target, (0, 0, 1), 500
    )
    candidate_status, candidate_value = candidate_search_port_bounded(
        target, (0, 0, 1), 500
    )
    initial_values.append(
        (target, source_value, candidate_value, steps, source_status, candidate_status)
    )

print("scan_domain_cases:", scan_cases)
print("scan_mismatch_count:", len(scan_mismatches))
print("scan_mismatches:", scan_mismatches[:10])
print("frozen_definition_equation_failure_count:", len(definition_failures))
print("frozen_definition_equation_failures:", definition_failures[:10])
print("terminating_search_cases:", search_cases)
print("candidate_vs_source_search_mismatch_count:", len(search_mismatches))
print("candidate_vs_source_search_mismatches:", search_mismatches[:10])
print("terminating_recurrence_cases:", recurrence_cases)
print("search_recurrence_failure_count:", len(recurrence_failures))
print("search_recurrence_failures:", recurrence_failures[:10])
print("exit_boundary_cases:", exit_cases)
print("exit_boundary_failure_count:", len(exit_failures))
print("exit_boundary_failures:", exit_failures[:10])
print("initial_prime_fibonacci_values:")
for item in initial_values:
    print(" ", item)

# Counterfactual mutations must visibly disagree with the frozen execution.
print("counterfactual_constant_scan_on_prime_5:", False, "expected", source_scan(5, 2, True))
print(
    "counterfactual_projection_search_for_target_2:",
    1,
    "expected",
    source_search_bounded(2, (0, 0, 1), 500)[1],
)
print(
    "counterfactual_reversed_divisibility_on_5:",
    False,
    "expected",
    source_scan(5, 2, True),
)

assert not scan_mismatches
assert not definition_failures
assert not search_mismatches
assert not recurrence_failures
assert not exit_failures
assert all(x[1] == x[2] and x[4] == x[5] == "reached" for x in initial_values)
