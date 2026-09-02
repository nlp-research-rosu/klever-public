from dataclasses import dataclass
from math import isqrt


def source_prime_scan(a: int, d: int, flag: bool) -> bool:
    while d * d <= a:
        if a % d == 0:
            flag = False
        d += 1
    return flag


def candidate_prime_scan_loop(a: int, d: int, fuel: int) -> bool:
    if fuel == 0:
        return True
    if d * d > a:
        return True
    if a % d == 0:
        return False
    return candidate_prime_scan_loop(a, d + 1, fuel - 1)


def candidate_prime_scan(a: int, d: int, flag: bool) -> bool:
    if not flag:
        return False
    start = 2 if d < 2 else d
    return candidate_prime_scan_loop(a, start, max(a, 0) + 1)


@dataclass(frozen=True)
class State:
    count: int
    a: int
    b: int


def prime_bit(value: int) -> int:
    return int(source_prime_scan(value, 2, value >= 2))


def advance(state: State) -> State:
    return State(
        count=state.count + prime_bit(state.b),
        a=state.b,
        b=state.a + state.b,
    )


def state_after(steps: int, initial: State) -> State:
    state = initial
    for _ in range(steps):
        state = advance(state)
    return state


def first_reach_within(
    target: int, initial: State, fuel: int
) -> int:
    state = initial
    for _ in range(fuel):
        if target <= state.count:
            return state.a
        state = advance(state)
    return state.a


def first_reaching_step(
    target: int, initial: State, limit: int
) -> int | None:
    state = initial
    for step in range(limit + 1):
        if target <= state.count:
            return step
        state = advance(state)
    return None


def source_search(
    target: int, initial: State, limit: int
) -> int | None:
    step = first_reaching_step(target, initial, limit)
    return None if step is None else state_after(step, initial).a


def candidate_search_with_witness(
    target: int, initial: State, witness_step: int
) -> int:
    if target <= initial.count:
        return initial.a
    next_state = advance(initial)
    if target <= next_state.count:
        return next_state.a
    return first_reach_within(target, next_state, witness_step)


def candidate_search_known_no_reach(
    target: int, initial: State
) -> int:
    if target <= initial.count:
        return initial.a
    next_state = advance(initial)
    if target <= next_state.count:
        return next_state.a
    # This is candidate semanticSearch's `else initial.a`, where its
    # `initial` argument is the public function's already-advanced state.
    return next_state.a


scan_cases = 0
scan_mismatches = []
bad_constant_false_mismatches = 0
bad_zero_fuel_mismatches = 0
for a in range(-20, 501):
    for d in range(2, 51):
        for flag in (False, True):
            expected = source_prime_scan(a, d, flag)
            observed = candidate_prime_scan(a, d, flag)
            scan_cases += 1
            if observed != expected:
                scan_mismatches.append((a, d, flag, expected, observed))
            if False != expected:
                bad_constant_false_mismatches += 1
            bad_zero_fuel = False if not flag else True
            if bad_zero_fuel != expected:
                bad_zero_fuel_mismatches += 1

search_cases = 0
search_mismatches = []
choice_mismatches = []
bad_return_b_mismatches = 0
bad_return_a_mismatches = 0
for count in range(0, 4):
    for target in range(max(1, count + 1), count + 3):
        for a in range(0, 21):
            for b in range(1, 21):
                initial = State(count, a, b)
                first_step = first_reaching_step(target, initial, 18)
                if first_step is None:
                    continue
                expected = state_after(first_step, initial).a
                search_cases += 1
                for extra in (0, 1, 3, 7):
                    witness = first_step + extra
                    if state_after(witness, initial).count < target:
                        continue
                    observed = candidate_search_with_witness(
                        target, initial, witness
                    )
                    if observed != expected:
                        choice_mismatches.append(
                            (
                                target,
                                initial,
                                first_step,
                                witness,
                                expected,
                                observed,
                            )
                        )
                canonical = candidate_search_with_witness(
                    target, initial, first_step
                )
                if canonical != expected:
                    search_mismatches.append(
                        (target, initial, first_step, expected, canonical)
                    )
                if initial.b != expected:
                    bad_return_b_mismatches += 1
                if initial.a != expected:
                    bad_return_a_mismatches += 1

humaneval_expected = [2, 3, 5, 13, 89]
humaneval_observed = []
for target in range(1, 6):
    initial = State(0, 0, 1)
    step = first_reaching_step(target, initial, 40)
    assert step is not None
    humaneval_observed.append(
        candidate_search_with_witness(target, initial, step)
    )

adversarial = [
    (-7, 2, True),
    (2, 2, True),
    (4, 2, True),
    (5, 2, True),
    (9, 2, True),
    (25, 3, True),
    (49, 5, True),
    (6, 4, True),
    (500, 23, False),
]

print("primeScan cases", scan_cases)
print("primeScan mismatches", len(scan_mismatches))
print("primeScan mismatch samples", scan_mismatches[:10])
print(
    "constant-false scan counterfactual mismatches",
    bad_constant_false_mismatches,
)
print(
    "zero-fuel scan counterfactual mismatches",
    bad_zero_fuel_mismatches,
)
print("adversarial primeScan witnesses")
for case in adversarial:
    print(
        case,
        "source",
        source_prime_scan(*case),
        "candidate",
        candidate_prime_scan(*case),
    )
print("search terminating cases", search_cases)
print("search mismatches", len(search_mismatches))
print("choice-witness independence mismatches", len(choice_mismatches))
print(
    "return-b search counterfactual mismatches",
    bad_return_b_mismatches,
)
print(
    "return-a search counterfactual mismatches",
    bad_return_a_mismatches,
)
print("HumanEval expected", humaneval_expected)
print("HumanEval observed", humaneval_observed)
print("HumanEval match", humaneval_observed == humaneval_expected)
divergent_old = State(0, 4, 4)
divergent_updated = advance(divergent_old)
divergent_old_value = candidate_search_known_no_reach(1, divergent_old)
divergent_updated_value = candidate_search_known_no_reach(
    1, divergent_updated
)
print("DIVERGENT RECURRENCE WITNESS")
print("target", 1)
print("old state", divergent_old)
print("updated state", divergent_updated)
print(
    "first 20 B values",
    [state_after(step, divergent_old).b for step in range(20)],
)
print(
    "first 20 counts",
    [state_after(step, divergent_old).count for step in range(20)],
)
print(
    "multiple-of-four invariant first 20",
    all(
        state_after(step, divergent_old).a % 4 == 0
        and state_after(step, divergent_old).b % 4 == 0
        for step in range(20)
    ),
)
print("candidate old value", divergent_old_value)
print("candidate updated value", divergent_updated_value)
print(
    "frozen recurrence equality holds",
    divergent_updated_value == divergent_old_value,
)
print("fuel upper-bound spot checks")
for a in (-10, 0, 1, 2, 10, 100, 500):
    transitions = 0 if a < 0 else max(0, isqrt(a) - 1)
    fuel = max(a, 0) + 1
    print(a, "max scan transitions from d=2", transitions, "fuel", fuel)
