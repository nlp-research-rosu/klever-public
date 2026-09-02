from functools import lru_cache

from solution import fib


@lru_cache(maxsize=None)
def recursive_oracle(n: int) -> int:
    if n < 2:
        return n
    return recursive_oracle(n - 1) + recursive_oracle(n - 2)


cases = list(range(31))
mismatches = [
    (n, fib(n), recursive_oracle(n))
    for n in cases
    if fib(n) != recursive_oracle(n)
]

print(f"cases={cases[0]}..{cases[-1]}")
print(f"mismatches={len(mismatches)}")
if mismatches:
    print(mismatches)
    raise SystemExit(1)
