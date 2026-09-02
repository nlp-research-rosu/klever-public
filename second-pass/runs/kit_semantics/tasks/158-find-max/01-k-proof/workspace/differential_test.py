from itertools import permutations
from random import Random

from solution import find_max


def oracle(words):
    if not words:
        return ""
    return sorted(words, key=lambda word: (-len(set(word)), word))[0]


cases = [
    ["name", "of", "string"],
    ["name", "enam", "game"],
    ["aaaaaaa", "bb", "cc"],
    [],
    ["é", "e", "😀"],
]

pool = ["", "a", "b", "aa", "ab", "ba", "abc"]
for size in range(1, 5):
    cases.extend(list(items) for items in permutations(pool, size))

rng = Random(20260729)
alphabet = "abcxyz"
universe = [""]
for _ in range(80):
    universe.append(
        "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 9)))
    )
universe = sorted(set(universe))
for _ in range(5000):
    size = rng.randrange(0, min(12, len(universe)) + 1)
    cases.append(rng.sample(universe, size))

mismatches = []
for words in cases:
    actual = find_max(words)
    expected = oracle(words)
    if actual != expected:
        mismatches.append((words, actual, expected))

print(f"cases={len(cases)} mismatches={len(mismatches)}")
if mismatches:
    print(mismatches[:10])
    raise SystemExit(1)
