#!/usr/bin/env python3
"""Independent finite witnesses for the frozen source/summary correspondence."""

from itertools import product


def source_program(values: tuple[int, ...]) -> bool:
    """Direct transcription of solution.py, without importing candidate code."""

    def helper(rest: tuple[int, ...]) -> bool:
        if len(rest) < 3:
            return True
        if rest[0] == rest[1]:
            return False
        if rest[0] == rest[2]:
            return False
        if rest[1] == rest[2]:
            return False
        return helper(rest[1:])

    if len(values) < 3:
        return False
    return helper(values)


def distinct3(a: int, b: int, c: int) -> bool:
    return a != b and a != c and b != c


def all_triples(values: tuple[int, ...]) -> bool:
    if len(values) < 3:
        return True
    return distinct3(values[0], values[1], values[2]) and all_triples(values[1:])


def happy(values: tuple[int, ...]) -> bool:
    if len(values) < 3:
        return False
    return all_triples(values)


def direct_prompt_oracle(values: tuple[int, ...]) -> bool:
    return len(values) >= 3 and all(
        len(set(values[index:index + 3])) == 3
        for index in range(len(values) - 2)
    )


def first_window_only(values: tuple[int, ...]) -> bool:
    return len(values) >= 3 and distinct3(values[0], values[1], values[2])


def globally_distinct(values: tuple[int, ...]) -> bool:
    return len(values) >= 3 and len(set(values)) == len(values)


def omits_second_third_check(values: tuple[int, ...]) -> bool:
    if len(values) < 3:
        return False
    return all(
        values[index] != values[index + 1]
        and values[index] != values[index + 2]
        for index in range(len(values) - 2)
    )


def rejects_length_three(values: tuple[int, ...]) -> bool:
    return len(values) > 3 and all_triples(values)


def main() -> None:
    checked = 0
    for size in range(9):
        for values in product((0, 1, 2), repeat=size):
            checked += 1
            observed = source_program(values)
            assert observed == happy(values)
            assert observed == direct_prompt_oracle(values)

    boundary_examples = [
        (),
        (97,),
        (97, 98),
        (97, 98, 99),
        (97, 97, 98),
        (97, 98, 97),
        (97, 98, 99, 99),
        (97, 98, 99, 97),
        (-1, 0, 1, -1),
        (0x10FFFF, 0, 1),
    ]
    print(f"exhaustive alphabet=(0,1,2), lengths=0..8, cases={checked}, mismatches=0")
    for values in boundary_examples:
        print(
            "boundary",
            values,
            "source=", source_program(values),
            "summary=", happy(values),
            "oracle=", direct_prompt_oracle(values),
        )

    mutations = [
        ("short strings accepted", lambda values: len(values) < 3 or happy(values)),
        ("first window only", first_window_only),
        ("global distinctness", globally_distinct),
        ("omit positions 1=2 check", omits_second_third_check),
        ("reject length exactly 3", rejects_length_three),
    ]
    search_space = [
        values
        for size in range(6)
        for values in product((0, 1, 2, 3), repeat=size)
    ]
    for label, mutation in mutations:
        witness = next(
            values
            for values in search_space
            if mutation(values) != direct_prompt_oracle(values)
        )
        print(
            "counterfactual",
            label,
            "witness=", witness,
            "mutated=", mutation(witness),
            "required=", direct_prompt_oracle(witness),
        )


if __name__ == "__main__":
    main()
