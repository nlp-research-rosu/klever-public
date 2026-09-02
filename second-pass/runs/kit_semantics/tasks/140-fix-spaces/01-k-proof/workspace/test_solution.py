from itertools import product

from solution import fix_spaces


def oracle(text):
    pieces = []
    index = 0
    while index < len(text):
        if text[index] != " ":
            pieces.append(text[index])
            index += 1
        else:
            end = index
            while end < len(text) and text[end] == " ":
                end += 1
            width = end - index
            pieces.append("-" if width > 2 else "_" * width)
            index = end
    return "".join(pieces)


examples = {
    "Example": "Example",
    "Example 1": "Example_1",
    " Example 2": "_Example_2",
    " Example   3": "_Example-3",
}

for text, expected in examples.items():
    actual = fix_spaces(text)
    assert actual == expected, (text, actual, expected)

checked = 0
for length in range(8):
    for chars in product(" aB", repeat=length):
        text = "".join(chars)
        actual = fix_spaces(text)
        expected = oracle(text)
        assert actual == expected, (text, actual, expected)
        checked += 1

print(
    "Python examples: 4/4; exhaustive strings over "
    f"{{space,a,B}} of length 0..7: {checked} checked, 0 mismatches"
)
