#!/usr/bin/env python3
"""Finite adversarial check of the Stage 3 summary equations.

This reimplements the frozen source algorithm and the K helper recurrences
without importing or executing any candidate or provenance Python file.
"""

from itertools import product


def words(alphabet: str, maximum_length: int):
    for length in range(maximum_length + 1):
        for characters in product(alphabet, repeat=length):
            yield "".join(characters)


def source_algorithm(a: str, b: str):
    found = b in a
    rotation = b
    current = ""
    for current in b[:-1]:
        rotation = rotation[1:] + current
        found = found or rotation in a
    return found, rotation, current


def rotate_with(rotation: str, character: str) -> str:
    return rotation[1:] + character


def cyc_scan(a: str, remaining: str, rotation: str, found: bool) -> bool:
    for character in remaining:
        rotation = rotate_with(rotation, character)
        found = found or rotation in a
    return found


def final_rotation(remaining: str, rotation: str) -> str:
    for character in remaining:
        rotation = rotate_with(rotation, character)
    return rotation


def final_char(remaining: str, current: str) -> str:
    for character in remaining:
        current = character
    return current


def cyc_pattern(a: str, b: str) -> bool:
    return cyc_scan(a, b[:-1], b, b in a)


def identity_rotation_scan(a: str, remaining: str, rotation: str, found: bool):
    for _character in remaining:
        found = found or rotation in a
    return found


def check() -> None:
    cases = 0
    mismatches = []
    for a in words("ab", 5):
        for b in words("ab", 5):
            expected_found, expected_rotation, expected_current = source_algorithm(a, b)
            observed = (
                cyc_pattern(a, b),
                final_rotation(b[:-1], b),
                final_char(b[:-1], ""),
            )
            expected = (expected_found, expected_rotation, expected_current)
            cases += 1
            if observed != expected:
                mismatches.append((a, b, expected, observed))

    identity_witness = None
    for a in words("ab", 4):
        for b in words("ab", 4):
            actual = cyc_pattern(a, b)
            mutant = identity_rotation_scan(a, b[:-1], b, b in a)
            if actual != mutant:
                identity_witness = (a, b, actual, mutant)
                break
        if identity_witness is not None:
            break

    full_iteration_state_witness = None
    for b in words("abc", 4):
        actual = final_rotation(b[:-1], b)
        mutant = final_rotation(b, b)
        if actual != mutant:
            full_iteration_state_witness = (b, actual, mutant)
            break

    print(f"cases={cases}")
    print(f"mismatch_count={len(mismatches)}")
    print(f"first_mismatch={mismatches[0] if mismatches else None}")
    print(f"identity_rotation_mutation_witness={identity_witness}")
    print(f"full_B_iteration_state_mutation_witness={full_iteration_state_witness}")


if __name__ == "__main__":
    check()
