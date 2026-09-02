"""Finite adversarial checks for every algebraic family in verification.k.

These checks supplement, but do not replace, the rule-by-rule mathematical
review. A nonzero result would provide a concrete false-rule witness.
"""

from __future__ import annotations

import itertools


NON_INT = "non-int"


def py_mod(n: int, divisor: int) -> int:
    return ((n % divisor) + divisor) % divisor


def collatz_next(n: int) -> int:
    if py_mod(n, 2) == 0:
        return (n - py_mod(n, 2)) // 2
    if py_mod(n, 2) == 1:
        return 3 * n + 1
    raise AssertionError("unreachable parity")


def valid_trace(values: tuple[object, ...]) -> bool:
    return bool(values) and all(
        isinstance(left, int)
        and not isinstance(left, bool)
        and isinstance(right, int)
        and not isinstance(right, bool)
        and right == collatz_next(left)
        for left, right in zip(values, values[1:])
    ) and isinstance(values[-1], int) and not isinstance(values[-1], bool)


def trace_first(values: tuple[object, ...]) -> int:
    return (
        values[0]
        if values
        and isinstance(values[0], int)
        and not isinstance(values[0], bool)
        else 0
    )


def trace_last(values: tuple[object, ...]) -> int:
    return (
        values[-1]
        if values
        and isinstance(values[-1], int)
        and not isinstance(values[-1], bool)
        else 0
    )


def maybe_odd(n: int) -> tuple[int, ...]:
    return () if py_mod(n, 2) == 0 else (n,)


def odd_without_last(values: tuple[object, ...]) -> tuple[int, ...]:
    return tuple(
        value
        for value in values[:-1]
        if isinstance(value, int)
        and not isinstance(value, bool)
        and py_mod(value, 2) == 1
    )


def fail(name: str, witness: object) -> None:
    raise AssertionError(f"{name} false witness: {witness!r}")


def main() -> None:
    integers = tuple(range(-20, 21))
    values: tuple[object, ...] = (-2, -1, 0, 1, 2, 3, NON_INT)
    sequences = [
        sequence
        for length in range(5)
        for sequence in itertools.product(values, repeat=length)
    ]

    # collatzNext and maybeOdd guarded equation coverage/disjointness.
    for n in integers:
        guards = [py_mod(n, 2) == 0, py_mod(n, 2) == 1]
        if sum(guards) != 1:
            fail("collatzNext/maybeOdd parity coverage", n)
        expected = n // 2 if n % 2 == 0 else 3 * n + 1
        if collatz_next(n) != expected:
            fail("collatzNext equation", n)
        expected_maybe = () if n % 2 == 0 else (n,)
        if maybe_odd(n) != expected_maybe:
            fail("maybeOdd equation", n)

    # Base/recursive/owise families for all finite test sequences.
    for sequence in sequences:
        expected_valid = (
            len(sequence) >= 1
            and all(
                isinstance(value, int) and not isinstance(value, bool)
                for value in sequence
            )
            and all(
                right == (left // 2 if left % 2 == 0 else 3 * left + 1)
                for left, right in zip(sequence, sequence[1:])
            )
        )
        if valid_trace(sequence) != expected_valid:
            fail("validCollatzTrace constructor rules", sequence)
        expected_first = (
            sequence[0]
            if sequence
            and isinstance(sequence[0], int)
            and not isinstance(sequence[0], bool)
            else 0
        )
        expected_last = (
            sequence[-1]
            if sequence
            and isinstance(sequence[-1], int)
            and not isinstance(sequence[-1], bool)
            else 0
        )
        if trace_first(sequence) != expected_first:
            fail("traceFirstInt constructor/owise rules", sequence)
        if trace_last(sequence) != expected_last:
            fail("traceLastInt constructor/owise rules", sequence)
        expected_odds = tuple(
            value
            for value in sequence[:-1]
            if isinstance(value, int)
            and not isinstance(value, bool)
            and value % 2 == 1
        )
        if odd_without_last(sequence) != expected_odds:
            fail("oddWithoutLast constructor/owise rules", sequence)

    # All seven proof-local concat/append simplification laws.
    short = [sequence for sequence in sequences if len(sequence) <= 2]
    for a, b, c in itertools.product(short, repeat=3):
        if a + () != a:
            fail("valSeqConcat right identity", a)
        if (a + b) + c != a + (b + c):
            fail("valSeqConcat associativity", (a, b, c))
    for a in sequences:
        for value in values:
            if a + (value,) == ():
                fail("nonempty concat != empty (left)", (a, value))
            if () == a + (value,):
                fail("nonempty concat != empty (right)", (a, value))
        if a:
            for j in integers:
                appended = a + (j,)
                if trace_first(appended) != trace_first(a):
                    fail("traceFirstInt append law", (a, j))
                if trace_last(appended) != j:
                    fail("traceLastInt append law", (a, j))
                if valid_trace(appended) != (
                    valid_trace(a) and j == collatz_next(trace_last(a))
                ):
                    fail("validCollatzTrace append law", (a, j))
        if valid_trace(a):
            for j in integers:
                appended = a + (j,)
                expected = odd_without_last(a) + maybe_odd(trace_last(a))
                if odd_without_last(appended) != expected:
                    fail("oddWithoutLast append law", (a, j))

    print(
        "checked",
        {
            "integers": len(integers),
            "sequences": len(sequences),
            "concat_triples": len(short) ** 3,
            "rule_families": 12,
            "false_witnesses": 0,
        },
    )


if __name__ == "__main__":
    main()

