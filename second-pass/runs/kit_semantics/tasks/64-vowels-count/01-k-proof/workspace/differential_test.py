from itertools import product

from solution import vowels_count


def oracle(word):
    ordinary = sum(1 for char in word if char.lower() in "aeiou")
    terminal_y = int(word[-1:].lower() == "y")
    return ordinary + terminal_y


examples = {
    "": 0,
    "abcde": 2,
    "ACEDY": 3,
    "yyy": 1,
    "rhythm": 0,
    "AEIOU": 5,
    "sky": 1,
    "yellow": 2,
}

checked = 0
mismatches = 0
for word, expected in examples.items():
    checked += 1
    mismatches += vowels_count(word) != expected

alphabet = "aAeEiIoOuUyYbz"
for length in range(5):
    for chars in product(alphabet, repeat=length):
        word = "".join(chars)
        checked += 1
        mismatches += vowels_count(word) != oracle(word)

print("checked:", checked)
print("mismatches:", mismatches)
assert mismatches == 0
