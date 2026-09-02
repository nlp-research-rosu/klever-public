from itertools import product
from string import ascii_letters

from solution import encode


def oracle(message):
    result = ""
    for character in message:
        code = ord(character)
        if 97 <= code <= 122:
            swapped = chr(code - 32)
        elif 65 <= code <= 90:
            swapped = chr(code + 32)
        else:
            swapped = character

        if swapped in "aeiouAEIOU":
            swapped = chr(ord(swapped) + 2)
        result += swapped
    return result


alphabet = ascii_letters + " "
checked = 0
mismatches = 0

for length in range(4):
    for characters in product(alphabet, repeat=length):
        message = "".join(characters)
        expected = oracle(message)
        actual = encode(message)
        checked += 1
        if actual != expected:
            mismatches += 1
            raise AssertionError((message, actual, expected))

for message in ("test", "This is a message"):
    expected = oracle(message)
    actual = encode(message)
    checked += 1
    if actual != expected:
        mismatches += 1
        raise AssertionError((message, actual, expected))

print(f"differential: checked={checked} mismatches={mismatches}")
