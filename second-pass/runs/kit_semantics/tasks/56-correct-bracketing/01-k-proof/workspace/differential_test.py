from itertools import product

from solution import correct_bracketing


def stack_oracle(brackets):
    stack = []
    for bracket in brackets:
        if bracket == "<":
            stack.append(bracket)
        elif stack:
            stack.pop()
        else:
            return False
    return not stack


checked = 0
mismatches = []
for length in range(9):
    for chars in product("<>", repeat=length):
        sample = "".join(chars)
        expected = stack_oracle(sample)
        actual = correct_bracketing(sample)
        checked += 1
        if actual != expected:
            mismatches.append((sample, expected, actual))

print(f"checked={checked} mismatches={len(mismatches)}")
assert not mismatches
