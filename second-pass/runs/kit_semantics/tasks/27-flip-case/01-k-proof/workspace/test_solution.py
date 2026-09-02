from solution import flip_case


def ascii_oracle(text: str) -> str:
    result = ""
    for character in text:
        code = ord(character)
        if 65 <= code <= 90:
            result += chr(code + 32)
        elif 97 <= code <= 122:
            result += chr(code - 32)
        else:
            result += character
    return result


cases = [
    "",
    "Hello",
    "aZ 123!?",
    "".join(chr(code) for code in range(128)),
    "HumanEval flip_case AaZz 019",
]

for case in cases:
    actual = flip_case(case)
    expected = ascii_oracle(case)
    assert actual == expected, (case, actual, expected)

# Curated non-ASCII witnesses exercise CPython's broader Unicode behavior.
assert flip_case("éÉ") == "Éé"
assert flip_case("ß") == "SS"

print(f"PASS: {len(cases)} ASCII cases and 2 Unicode witnesses")
