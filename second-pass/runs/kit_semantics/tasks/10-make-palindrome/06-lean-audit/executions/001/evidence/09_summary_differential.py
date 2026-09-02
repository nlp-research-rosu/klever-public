#!/usr/bin/env python3
"""Finite adversarial check of the frozen K summary recurrences."""

from __future__ import annotations

from itertools import product


Seq = tuple[int, ...]


def source_program(string: Seq) -> Seq:
    reverse_string: Seq = ()
    for char in string:
        reverse_string = (char,) + reverse_string

    prefix: Seq = ()
    reverse_prefix: Seq = ()
    found = string == reverse_string
    result = string if found else string + reverse_string

    for char in string:
        if not found:
            prefix = prefix + (char,)
            reverse_prefix = (char,) + reverse_prefix
            if string + reverse_prefix == prefix + reverse_string:
                result = string + reverse_prefix
                found = True
    return result


def reverse_acc(remaining: Seq, accumulator: Seq) -> Seq:
    if not remaining:
        return accumulator
    return reverse_acc(remaining[1:], (remaining[0],) + accumulator)


def search_result(
    source: Seq,
    remaining: Seq,
    prefix: Seq,
    reverse_prefix: Seq,
    reverse: Seq,
    found: bool,
    result: Seq,
) -> Seq:
    if found:
        return result
    if not remaining:
        return result
    char, rest = remaining[0], remaining[1:]
    new_prefix = prefix + (char,)
    new_reverse_prefix = (char,) + reverse_prefix
    if new_prefix + reverse == source + new_reverse_prefix:
        return source + new_reverse_prefix
    return search_result(
        source,
        rest,
        new_prefix,
        new_reverse_prefix,
        reverse,
        False,
        result,
    )


def complete_pal(source: Seq) -> Seq:
    reverse = reverse_acc(source, ())
    pal = source == reverse
    seed = source if pal else source + reverse
    return search_result(source, source, (), (), reverse, pal, seed)


def independent_shortest_oracle(source: Seq) -> Seq:
    for prefix_length in range(len(source) + 1):
        candidate = source + tuple(reversed(source[:prefix_length]))
        if candidate == tuple(reversed(candidate)):
            return candidate
    raise AssertionError("the whole-source extension must be a palindrome")


def identity_reverse_mutant(source: Seq) -> Seq:
    reverse = source
    pal = source == reverse
    seed = source if pal else source + reverse
    return search_result(source, source, (), (), reverse, pal, seed)


def inequality_search_mutant(source: Seq) -> Seq:
    reverse = reverse_acc(source, ())
    found = source == reverse
    result = source if found else source + reverse
    prefix: Seq = ()
    reverse_prefix: Seq = ()
    for char in source:
        if not found:
            prefix = prefix + (char,)
            reverse_prefix = (char,) + reverse_prefix
            if source + reverse_prefix != prefix + reverse:
                result = source + reverse_prefix
                found = True
    return result


def main() -> None:
    samples = [
        sequence
        for length in range(8)
        for sequence in product(range(3), repeat=length)
    ]
    summary_mismatches = []
    oracle_mismatches = []
    identity_mutant_mismatches = []
    inequality_mutant_mismatches = []
    for sample in samples:
        source = source_program(sample)
        summary = complete_pal(sample)
        oracle = independent_shortest_oracle(sample)
        if summary != source:
            summary_mismatches.append((sample, source, summary))
        if source != oracle:
            oracle_mismatches.append((sample, source, oracle))
        if identity_reverse_mutant(sample) != source:
            identity_mutant_mismatches.append(sample)
        if inequality_search_mutant(sample) != source:
            inequality_mutant_mismatches.append(sample)

    adversarial = [
        (),
        (0,),
        (0, 1),
        (0, 1, 0),
        (0, 1, 1),
        (0, 1, 2, 0),
        (0, 0, 1, 0, 0, 2),
    ]
    print(f"exhaustive alphabet={{0,1,2}} lengths=0..7 samples={len(samples)}")
    print(f"K-summary/source mismatches={len(summary_mismatches)}")
    print(f"source/shortest-palindrome-oracle mismatches={len(oracle_mismatches)}")
    print(
        "identity-reverse counterfactual mismatches="
        f"{len(identity_mutant_mismatches)}"
    )
    print(
        "inequality-search counterfactual mismatches="
        f"{len(inequality_mutant_mismatches)}"
    )
    print("adversarial examples:")
    for sample in adversarial:
        print(
            f"  {sample} -> source={source_program(sample)} "
            f"summary={complete_pal(sample)} "
            f"oracle={independent_shortest_oracle(sample)}"
        )

    assert not summary_mismatches
    assert not oracle_mismatches
    assert identity_mutant_mismatches
    assert inequality_mutant_mismatches
    print("FINITE ADVERSARIAL CHECK PASSED")


if __name__ == "__main__":
    main()
