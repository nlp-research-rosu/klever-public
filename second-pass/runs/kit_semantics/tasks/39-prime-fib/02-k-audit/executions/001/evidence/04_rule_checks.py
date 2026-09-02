#!/usr/bin/env python3
"""Bounded counterexample search for every proof-local summary equation."""

from __future__ import annotations


def py_mod(a: int, d: int) -> int:
    return ((a % d) + d) % d


def prime_scan(a: int, d: int, p: bool) -> bool:
    while d * d <= a:
        if py_mod(a, d) == 0:
            p = False
        d += 1
    return p


checks = [0, 0, 0, 0]
for a in range(0, 121):
    for d in range(2, 17):
        for p in (False, True):
            if d * d > a:
                assert prime_scan(a, d, p) == p
                checks[0] += 1
            if d * d <= a and py_mod(a, d) == 0:
                assert prime_scan(a, d, p) is False
                checks[1] += 1
            if d * d <= a and py_mod(a, d) != 0:
                assert prime_scan(a, d + 1, p) == prime_scan(a, d, p)
                checks[2] += 1
            assert prime_scan(a, d, False) is False
            checks[3] += 1
print("primeScan rule witnesses checked:", checks)


def bit(b: int) -> int:
    return int(prime_scan(b, 2, b >= 2))


def search(n: int, c: int, a: int, b: int, limit: int = 100):
    for _ in range(limit):
        if c >= n:
            return a
        c, a, b = c + bit(b), b, a + b
    return None


# Test the base and boundary equations broadly, then test the fold equation at
# every state reached by the actual initial Fibonacci search for N=1..8.
# These are finite checks supporting the accompanying static proof.
search_checks = [0, 0, 0]
for n in range(1, 6):
    for c in range(n, n + 3):
        for a in range(0, 8):
            for b in range(1, 9):
                current = search(n, c, a, b)
                assert current == a
                search_checks[0] += 1
    for b in range(1, 201):
        if bit(b):
            assert search(n, n - 1, 0, b) == b
            search_checks[1] += 1

for n in range(1, 9):
    c, a, b = 0, 0, 1
    while c < n:
        current = search(n, c, a, b)
        successor_state = (c + bit(b), b, a + b)
        successor = search(n, *successor_state)
        assert current is not None and successor == current
        search_checks[2] += 1
        c, a, b = successor_state
print("primeFibSearch rule witnesses checked:", search_checks)
print("counterexamples:", 0)
