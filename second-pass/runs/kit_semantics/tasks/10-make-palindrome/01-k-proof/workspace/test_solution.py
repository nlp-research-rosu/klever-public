import itertools
import random

from solution import make_palindrome


def oracle(string: str) -> str:
    for size in range(len(string) + 1):
        candidate = string + string[:size][::-1]
        if candidate == candidate[::-1]:
            return candidate
    raise AssertionError("the full-prefix completion must be palindromic")


cases = ["", "cat", "cata", "race", "abba", "🙂a", "åßç", "あいあ"]
for size in range(10):
    cases.extend("".join(chars) for chars in itertools.product("ab", repeat=size))

random.seed(20260729)
alphabet = "abcXYZ09🙂åßあ"
for _ in range(500):
    size = random.randrange(0, 25)
    cases.append("".join(random.choice(alphabet) for _ in range(size)))

mismatches = []
for case in cases:
    actual = make_palindrome(case)
    expected = oracle(case)
    if actual != expected:
        mismatches.append((case, actual, expected))

print(f"cases={len(cases)} mismatches={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:10]:
        print(repr(mismatch))
    raise SystemExit(1)
