from itertools import product

from solution import is_palindrome


def oracle(text: str) -> bool:
    left = 0
    right = len(text) - 1
    while left < right:
        if text[left] != text[right]:
            return False
        left += 1
        right -= 1
    return True


alphabet = ("a", "b", "é", "🙂")
cases = ["", "aba", "aaaaa", "zbcd"]
for length in range(6):
    cases.extend("".join(chars) for chars in product(alphabet, repeat=length))

mismatches = [
    (text, is_palindrome(text), oracle(text))
    for text in cases
    if is_palindrome(text) != oracle(text)
]

print(f"cases={len(cases)} mismatches={len(mismatches)}")
if mismatches:
    print(mismatches[:10])
    raise SystemExit(1)
