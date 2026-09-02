from itertools import product

from solution import total_match


def oracle(lst1, lst2):
    return lst1 if len("".join(lst1)) <= len("".join(lst2)) else lst2


atoms = ("", "a", "bc", "XYZ")
lists = []
for size in range(4):
    lists.extend([list(items) for items in product(atoms, repeat=size)])

prompt_cases = [
    ([], []),
    (["hi", "admin"], ["hI", "Hi"]),
    (["hi", "admin"], ["hi", "hi", "admin", "project"]),
    (["hi", "admin"], ["hI", "hi", "hi"]),
    (["4"], ["1", "2", "3", "4", "5"]),
]

tested = 0
mismatches = []
for lst1, lst2 in product(lists, repeat=2):
    expected = oracle(lst1, lst2)
    actual = total_match(lst1, lst2)
    tested += 1
    if actual is not expected:
        mismatches.append((lst1, lst2, expected, actual))

for lst1, lst2 in prompt_cases:
    expected = oracle(lst1, lst2)
    actual = total_match(lst1, lst2)
    tested += 1
    if actual is not expected:
        mismatches.append((lst1, lst2, expected, actual))

print(f"tested={tested} mismatches={len(mismatches)}")
if mismatches:
    raise AssertionError(mismatches[:5])
