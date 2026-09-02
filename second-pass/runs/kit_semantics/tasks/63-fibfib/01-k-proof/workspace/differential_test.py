from functools import lru_cache

from solution import fibfib


@lru_cache(maxsize=None)
def recursive_oracle(n: int) -> int:
    if n == 0 or n == 1:
        return 0
    if n == 2:
        return 1
    return (
        recursive_oracle(n - 1)
        + recursive_oracle(n - 2)
        + recursive_oracle(n - 3)
    )


inputs = list(range(31))
mismatches = [
    (n, fibfib(n), recursive_oracle(n))
    for n in inputs
    if fibfib(n) != recursive_oracle(n)
]

print(f"inputs: 0..{inputs[-1]}")
print(f"cases: {len(inputs)}")
print(f"mismatches: {len(mismatches)}")
if mismatches:
    print(mismatches)
    raise SystemExit(1)
