from itertools import product

from solution import check_dict_case


def contract_oracle(d):
    if not d:
        return False
    keys = tuple(d.keys())
    return (
        all(isinstance(k, str) and k.islower() for k in keys)
        or all(isinstance(k, str) and k.isupper() for k in keys)
    )


prompt_examples = [
    ({"a": "apple", "b": "banana"}, True),
    ({"a": "apple", "A": "banana", "B": "banana"}, False),
    ({"a": "apple", 8: "banana"}, False),
    ({"Name": "John", "Age": "36", "City": "Houston"}, False),
    ({"STATE": "NC", "ZIP": "12345"}, True),
]

key_pool = (
    "",
    "a",
    "abc",
    "A",
    "ABC",
    "a1",
    "A1",
    "123",
    "a-B",
    "é",
    "É",
    0,
    8,
    True,
    None,
    ("tuple",),
)

checks = 0
mismatches = 0

for d, expected in prompt_examples:
    got = check_dict_case(d)
    oracle = contract_oracle(d)
    checks += 1
    if got != expected or got != oracle:
        mismatches += 1
        print("PROMPT MISMATCH", repr(d), expected, oracle, got)

for size in range(4):
    for keys in product(key_pool, repeat=size):
        d = {key: index for index, key in enumerate(keys)}
        got = check_dict_case(d)
        oracle = contract_oracle(d)
        checks += 1
        if got != oracle:
            mismatches += 1
            print("CORPUS MISMATCH", repr(d), oracle, got)

print("checks =", checks)
print("mismatches =", mismatches)
if mismatches:
    raise SystemExit(1)
