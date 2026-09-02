import itertools
import random

from solution import is_bored


def oracle(text):
    sentences = []
    current = []
    for char in text:
        if char in ".?!":
            sentences.append("".join(current))
            current = []
        else:
            current.append(char)
    sentences.append("".join(current))

    total = 0
    for sentence in sentences:
        words = sentence.split()
        if words and words[0] == "I":
            total += 1
    return total


examples = [
    "Hello world",
    "The sky is blue. The sun is shining. I love this weather",
    "I am. You are! I? Idea. \tI\nagree",
    "You and I are going for a walk",
    "",
    "I",
    " . I ! ? I\twork",
]

checked = 0
for text in examples:
    assert is_bored(text) == oracle(text), repr(text)
    checked += 1

alphabet = ("I", "A", " ", "\t", "\n", ".", "?", "!")
for length in range(6):
    for chars in itertools.product(alphabet, repeat=length):
        text = "".join(chars)
        assert is_bored(text) == oracle(text), repr(text)
        checked += 1

rng = random.Random(20260730)
broad_alphabet = (
    "I",
    "A",
    "é",
    "中",
    " ",
    "\t",
    "\n",
    "\r",
    "\v",
    "\f",
    "\u00a0",
    ".",
    "?",
    "!",
)
for _ in range(5000):
    text = "".join(
        rng.choice(broad_alphabet) for _ in range(rng.randrange(0, 41))
    )
    assert is_bored(text) == oracle(text), repr(text)
    checked += 1

print(f"differential cases={checked} mismatches=0")
