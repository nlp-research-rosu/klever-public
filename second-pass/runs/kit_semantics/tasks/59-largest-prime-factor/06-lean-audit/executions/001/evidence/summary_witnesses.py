#!/usr/bin/env python3

def source_run(n: int) -> int:
    factor = 2
    steps = 0
    while n > factor:
        if n % factor == 0:
            n = n // factor
        else:
            factor = factor + 1
        steps += 1
        if steps > 100000:
            raise RuntimeError("unexpected nontermination")
    return n


def summary_run(n: int, factor: int) -> int:
    steps = 0
    while True:
        if n <= factor:
            return n
        py_mod = ((n % factor) + factor) % factor
        if py_mod == 0:
            n = (n - py_mod) // factor
        else:
            factor = factor + 1
        steps += 1
        if steps > 100000:
            raise RuntimeError("unexpected nontermination")


witnesses = [2, 3, 4, 6, 8, 9, 10, 12, 25, 49, 77, 97, 13195, 2048]
print("WITNESSES")
for n in witnesses:
    source = source_run(n)
    summary = summary_run(n, 2)
    print({"n": n, "source": source, "lpfFrom": summary, "equal": source == summary})
mismatches = [
    n for n in range(2, 5001) if source_run(n) != summary_run(n, 2)
]
print("RANGE 2..5000 mismatch_count", len(mismatches))
print("COUNTERFACTUAL divisible n=12,f=2 correct_next_n=6 mutated_next_n=", 7)
print("COUNTERFACTUAL nondivisible n=25,f=2 correct_next_f=3 mutated_next_f=", 4)
