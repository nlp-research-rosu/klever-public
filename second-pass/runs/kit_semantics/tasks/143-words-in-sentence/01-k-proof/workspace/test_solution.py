import random

from solution import words_in_sentence


def is_prime_oracle(n):
    if n < 2:
        return False
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 1
    return True


def oracle(sentence):
    return " ".join(
        word for word in sentence.split(" ") if is_prime_oracle(len(word))
    )


cases = [
    "This is a test",
    "lets go for swimming",
    "",
    " ",
    "  ",
    "a  bb   ccc",
    " aa ",
]

# Every possible single-word length in the prompt's length range.
cases.extend("a" * length for length in range(1, 101))

# Every pair of positive word lengths whose sentence fits the bound.
for left in range(1, 99):
    for right in range(1, 100 - left):
        cases.append("a" * left + " " + "b" * right)

# A deterministic broader sample over modeled ASCII letters and spaces.
rng = random.Random(20260725)
alphabet = "abcdefghijklmnopqrstuvwxyz "
for _ in range(2000):
    length = rng.randint(1, 100)
    cases.append("".join(rng.choice(alphabet) for _ in range(length)))

mismatches = []
for sentence in cases:
    actual = words_in_sentence(sentence)
    expected = oracle(sentence)
    if actual != expected:
        mismatches.append((sentence, actual, expected))

print(f"DIFFERENTIAL_CASES={len(cases)}")
print(f"DIFFERENTIAL_MISMATCHES={len(mismatches)}")
if mismatches:
    raise AssertionError(mismatches[:5])
