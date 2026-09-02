from itertools import product

from solution import will_it_fly


def oracle(q, w):
    balanced = all(q[i] == q[-i - 1] for i in range(len(q)))
    total = 0
    for value in q:
        total += value
    return balanced and total <= w


checked = 0
for length in range(6):
    for values in product(range(-2, 3), repeat=length):
        q = list(values)
        for w in range(-5, 6):
            assert will_it_fly(q, w) is oracle(q, w), (q, w)
            checked += 1

numeric_values = [False, True, -1, 0, 1, -0.5, 0.5]
numeric_weights = [-2, -0.5, 0, 0.5, 2]
for length in range(5):
    for values in product(numeric_values, repeat=length):
        q = list(values)
        for w in numeric_weights:
            assert will_it_fly(q, w) is oracle(q, w), (q, w)
            checked += 1

print(f"differential: {checked} cases, 0 mismatches")
