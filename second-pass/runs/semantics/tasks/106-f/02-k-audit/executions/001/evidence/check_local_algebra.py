#!/usr/bin/env python3
"""Finite witnesses for all four proof-local ValSeq simplification rules."""

from itertools import product


def sequences(alphabet, max_length):
    result = [()]
    for length in range(1, max_length + 1):
        result.extend(product(alphabet, repeat=length))
    return result


def main():
    seqs = sequences((0, 1), 4)
    checks = {
        "associativity": 0,
        "right_identity": 0,
        "left_cancellation": 0,
        "prefix_fixedpoint": 0,
    }
    failures = []

    for a in seqs:
        if a + () != a:
            failures.append(("right_identity", a))
        checks["right_identity"] += 1
        for b in seqs:
            if a + b == a + () and b != ():
                failures.append(("prefix_fixedpoint", a, b))
            checks["prefix_fixedpoint"] += 1
            for c in seqs:
                if (a + b) + c != a + (b + c):
                    failures.append(("associativity", a, b, c))
                checks["associativity"] += 1
                # The K rule is an implication: when equal prefixes cancel,
                # the suffixes must be equal.
                if a + b == a + c and b != c:
                    failures.append(("left_cancellation", a, b, c))
                checks["left_cancellation"] += 1

    print(f"SEQUENCE_DOMAIN: alphabet=[0,1], length=0..4, count={len(seqs)}")
    for name, count in checks.items():
        print(f"CHECK {name}: instances={count}")
    print(f"FAILURE_COUNT: {len(failures)}")
    for failure in failures[:20]:
        print("FAILURE:", failure)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
