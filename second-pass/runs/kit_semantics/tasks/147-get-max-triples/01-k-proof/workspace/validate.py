from itertools import combinations

from solution import get_max_triples


def brute_force(n):
    values = [i * i - i + 1 for i in range(1, n + 1)]
    return sum(
        1
        for triple in combinations(values, 3)
        if sum(triple) % 3 == 0
    )


def main():
    tested = list(range(1, 101))
    mismatches = [
        (n, get_max_triples(n), brute_force(n))
        for n in tested
        if get_max_triples(n) != brute_force(n)
    ]
    assert get_max_triples(5) == 1
    assert not mismatches, mismatches
    print(
        "oracle=direct array construction + itertools.combinations; "
        f"inputs=1..100; example_n=5; mismatches={len(mismatches)}"
    )


if __name__ == "__main__":
    main()
