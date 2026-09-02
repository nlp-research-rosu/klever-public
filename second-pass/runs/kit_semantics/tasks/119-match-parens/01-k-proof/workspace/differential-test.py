from itertools import product

from solution import match_parens


def is_balanced(text):
    depth = 0
    for character in text:
        if character == '(':
            depth += 1
        else:
            depth -= 1
        if depth < 0:
            return False
    return depth == 0


def oracle(pair):
    left, right = pair
    if is_balanced(left + right) or is_balanced(right + left):
        return 'Yes'
    return 'No'


def paren_strings(length):
    return (''.join(chars) for chars in product('()', repeat=length))


checked = 0
mismatches = []
for left_length in range(11):
    for right_length in range(11 - left_length):
        for left in paren_strings(left_length):
            for right in paren_strings(right_length):
                pair = [left, right]
                expected = oracle(pair)
                actual = match_parens(pair)
                checked += 1
                if actual != expected:
                    mismatches.append((pair, expected, actual))

assert not mismatches, mismatches[:10]
print(f'differential: {checked} pairs, {len(mismatches)} mismatches')
