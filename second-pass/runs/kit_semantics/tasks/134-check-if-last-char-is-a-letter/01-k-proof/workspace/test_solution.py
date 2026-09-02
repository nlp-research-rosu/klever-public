from itertools import product
from pathlib import Path

from solution import check_if_last_char_is_a_letter


def split_oracle(txt):
    final_word = txt.split(" ")[-1]
    return len(final_word) == 1 and final_word.isalpha()


solution_source = Path("solution.py").read_text(encoding="utf-8").rstrip()
smoke_source = Path("smoke.py").read_text(encoding="utf-8")
assert smoke_source.startswith(solution_source + "\n\n")


prompt_examples = {
    "apple pie": False,
    "apple pi e": True,
    "apple pi e ": False,
    "": False,
}

for text, expected in prompt_examples.items():
    assert check_if_last_char_is_a_letter(text) == expected
    assert split_oracle(text) == expected

alphabet = (" ", "a", "Z", "1", "!", "\t")
tested = 0
mismatches = []
for length in range(6):
    for chars in product(alphabet, repeat=length):
        text = "".join(chars)
        tested += 1
        actual = check_if_last_char_is_a_letter(text)
        expected = split_oracle(text)
        if actual != expected:
            mismatches.append((text, actual, expected))

unicode_cases = ("é", "x é", "éx", "λ", "x λ", "λ ")
for text in unicode_cases:
    tested += 1
    actual = check_if_last_char_is_a_letter(text)
    expected = split_oracle(text)
    if actual != expected:
        mismatches.append((text, actual, expected))

print(f"differential cases: {tested}")
print(f"mismatches: {len(mismatches)}")
print(
    "unicode witness 'é': "
    f"solution={check_if_last_char_is_a_letter('é')}, "
    f"oracle={split_oracle('é')}"
)
assert not mismatches
