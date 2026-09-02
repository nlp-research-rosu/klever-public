import re
from pathlib import Path


def arithmetic_palindrome(value):
    original = value
    reversed_value = 0
    while value:
        reversed_value = reversed_value * 10 + value % 10
        value //= 10
    return original == reversed_value


def independent_oracle(n):
    even = 0
    odd = 0
    for value in range(1, n + 1):
        if arithmetic_palindrome(value):
            if value % 2 == 0:
                even += 1
            else:
                odd += 1
    return even, odd


text = Path("spec.k").read_text(encoding="utf-8")
pattern = re.compile(
    r"claim \[(?P<label>[^\]]+)\]:"
    r".*?=> tuple\(vCons\((?P<even>\d+), "
    r"vCons\((?P<odd>\d+), \.ValSeq\)\)\)"
    r".*?requires (?P<lower>\d+) <=Int N andBool "
    r"N (?P<upper_op><=Int|<Int) (?P<upper>\d+)",
    re.DOTALL,
)

claims = list(pattern.finditer(text))
assert len(claims) == 108, len(claims)

coverage = {}
for match in claims:
    lower = int(match.group("lower"))
    upper = int(match.group("upper"))
    if match.group("upper_op") == "<=Int":
        upper += 1
    result = int(match.group("even")), int(match.group("odd"))
    for n in range(lower, upper):
        assert n not in coverage, (n, match.group("label"))
        coverage[n] = result

assert sorted(coverage) == list(range(1, 1001))
for n in range(1, 1001):
    assert coverage[n] == independent_oracle(n), (
        n,
        coverage[n],
        independent_oracle(n),
    )

print("claims_checked=108")
print("domain_covered=1..1000")
print("target_mismatches=0")
