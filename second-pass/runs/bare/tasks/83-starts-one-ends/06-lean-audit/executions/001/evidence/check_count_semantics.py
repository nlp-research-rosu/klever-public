#!/usr/bin/env python3


def brute_force_count(n: int) -> int:
    low = 1 if n == 1 else 10 ** (n - 1)
    high = 10**n
    return sum(
        1
        for value in range(low, high)
        if str(value).startswith("1") or str(value).endswith("1")
    )


def stage1_definitions(n: int) -> tuple[int, int, int, int]:
    if n == 1:
        return (0, 0, 0, 1)
    middle = 10 ** (n - 2)
    starts = 10 * middle
    ends = 9 * middle
    overlap = middle
    return starts, ends, overlap, starts + ends - overlap


def source_program_result(n: int) -> int:
    return 1 if n == 1 else 18 * 10 ** (n - 2)


for n in range(1, 7):
    starts, ends, overlap, qualifying = stage1_definitions(n)
    brute = brute_force_count(n)
    source = source_program_result(n)
    assert qualifying == brute == source
    print(
        f"n={n} starts={starts} ends={ends} overlap={overlap} "
        f"qualifying={qualifying} brute={brute} source={source}"
    )

# Counterfactual closed forms are discriminated at realizable positive inputs.
mutations = {
    "starts-factor-9": lambda n: (
        9 + 9 - 1
    ) * 10 ** (n - 2),
    "ends-factor-10": lambda n: (
        10 + 10 - 1
    ) * 10 ** (n - 2),
    "omit-overlap-subtraction": lambda n: (
        10 + 9
    ) * 10 ** (n - 2),
    "source-coefficient-17": lambda n: 17 * 10 ** (n - 2),
}
for name, mutation in mutations.items():
    witness = next(
        n
        for n in range(2, 5)
        if mutation(n) != brute_force_count(n)
    )
    print(
        f"counterfactual={name} witness_n={witness} "
        f"mutated={mutation(witness)} expected={brute_force_count(witness)} "
        "rejected=True"
    )

print("RESULT: PASS")
