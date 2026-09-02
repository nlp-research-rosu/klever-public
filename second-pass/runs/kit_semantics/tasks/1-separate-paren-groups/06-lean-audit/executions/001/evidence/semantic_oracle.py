#!/usr/bin/env python3

from itertools import product


SPACE = 32
OPEN = 40
CLOSE = 41


def source_program(codes):
    groups = []
    current = []
    depth = 0
    for char in codes:
        if char != SPACE:
            current.append(char)
            if char == OPEN:
                depth += 1
            else:
                depth -= 1
            if depth == 0:
                groups.append(tuple(current))
                current = []
    return tuple(groups)


def k_summary(codes, depth=0, current=(), output=()):
    if not codes:
        return output
    char, *rest = codes
    rest = tuple(rest)
    if char == SPACE:
        return k_summary(rest, depth, current, output)
    if char == OPEN:
        next_depth = depth + 1
    else:
        next_depth = depth - 1
    next_current = current + (char,)
    if next_depth == 0:
        return k_summary(rest, 0, (), output + (next_current,))
    return k_summary(rest, next_depth, next_current, output)


def independent_validity(codes):
    depth = 0
    for char in codes:
        if char == SPACE:
            continue
        if char == OPEN:
            depth += 1
        elif char == CLOSE and depth > 0:
            depth -= 1
        else:
            return False
    return depth == 0


def k_valid_suffix(codes, depth=0):
    if not codes:
        return depth == 0
    char, *rest = codes
    rest = tuple(rest)
    if char == SPACE:
        return k_valid_suffix(rest, depth)
    if char == OPEN:
        return k_valid_suffix(rest, depth + 1)
    if char == CLOSE and depth > 0:
        return k_valid_suffix(rest, depth - 1)
    if char == CLOSE and depth <= 0:
        return False
    return False


alphabet = (SPACE, OPEN, CLOSE, 65)
summary_mismatches = []
validity_mismatches = []
checked = 0
for length in range(7):
    for codes in product(alphabet, repeat=length):
        checked += 1
        source = source_program(codes)
        summary = k_summary(codes)
        if source != summary:
            summary_mismatches.append((codes, source, summary))
        independent = independent_validity(codes)
        modeled = k_valid_suffix(codes)
        if independent != modeled:
            validity_mismatches.append((codes, independent, modeled))

examples = [
    "",
    "   ",
    "()",
    "(())",
    "()()",
    "( ) (( )) (( )( ))",
    "(",
    ")",
    "(A)",
]
print(f"enumerated_sequences={checked}")
print(f"summary_mismatches={len(summary_mismatches)}")
print(f"validity_mismatches={len(validity_mismatches)}")
for example in examples:
    codes = tuple(map(ord, example))
    print(
        repr(example),
        "source=", source_program(codes),
        "summary=", k_summary(codes),
        "valid=", k_valid_suffix(codes),
    )

# Counterfactuals that the comparison must detect.
def wrong_open_mutation(codes):
    groups = []
    current = []
    depth = 0
    for char in codes:
        if char != SPACE:
            current.append(char)
            depth -= 1
            if depth == 0:
                groups.append(tuple(current))
                current = []
    return tuple(groups)


counterexample = tuple(map(ord, "()"))
print(
    "counterfactual_open_branch_detected=",
    wrong_open_mutation(counterexample) != source_program(counterexample),
)
