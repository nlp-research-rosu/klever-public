from itertools import product

from solution import count_distinct_characters


def oracle(text: str) -> int:
    lowered = text.lower()
    distinct = []
    for character in lowered:
        if character not in distinct:
            distinct.append(character)
    return len(distinct)


cases = [
    "",
    "xyzXYZ",
    "Jerry",
    "Aa!a",
    "İ",
    "Straße",
    "Σσς",
    "Hello, World!",
]
alphabet = "aA0!zZ"
for length in range(5):
    cases.extend("".join(chars) for chars in product(alphabet, repeat=length))

mismatches = [
    (text, count_distinct_characters(text), oracle(text))
    for text in cases
    if count_distinct_characters(text) != oracle(text)
]

print(f"cases={len(cases)} mismatches={len(mismatches)}")
print(
    "unicode_witness='İ' "
    f"lowered_code_points={[ord(character) for character in 'İ'.lower()]} "
    f"result={count_distinct_characters('İ')}"
)
if mismatches:
    print(mismatches[:10])
    raise SystemExit(1)
