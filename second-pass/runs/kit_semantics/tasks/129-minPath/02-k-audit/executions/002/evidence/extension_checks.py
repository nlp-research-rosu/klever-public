#!/usr/bin/env python3
"""Finite overlap/boundary checks for proof-local mathematical equations."""
import itertools
import json
import random
import sys

rng = random.Random(12951001)
failures = []
permutations_checked = 0
selector_checks = 0
neighbor_checks = 0

def grid_rows(p, n):
    return [p[i*n:(i+1)*n] for i in range(n)]

def one_pos(p, n):
    q = p.index(1)
    return q // n, q % n

def grid_at(p, n, i, j):
    return p[i*n+j]

def choose_min(base, value, enabled):
    return min(base, value) if enabled else base

def neighbor_summary(p, n, r, c):
    out = n*n+1
    for value, enabled in (
        (grid_at(p,n,r-1,c) if r > 0 else 0, r > 0),
        (grid_at(p,n,r+1,c) if r+1 < n else 0, r+1 < n),
        (grid_at(p,n,r,c-1) if c > 0 else 0, c > 0),
        (grid_at(p,n,r,c+1) if c+1 < n else 0, c+1 < n),
    ):
        out = choose_min(out, value, enabled)
    return out

def direct_neighbor(p, n, r, c):
    return min(grid_at(p,n,rr,cc) for rr,cc in ((r-1,c),(r+1,c),(r,c-1),(r,c+1)) if 0 <= rr < n and 0 <= cc < n)

samples = []
samples += [(2, list(p)) for p in itertools.permutations(range(1, 5))]
for n in range(3, 9):
    for _ in range(200):
        p = list(range(1, n*n+1))
        rng.shuffle(p)
        samples.append((n, p))

for n, p in samples:
    permutations_checked += 1
    rows = grid_rows(p, n)
    r, c = one_pos(p, n)
    if len(rows) != n or any(len(row) != n for row in rows):
        failures.append("gridRows length")
    if not (0 <= r < n and 0 <= c < n):
        failures.append("one position bounds")
    for i in range(n):
        for j in range(n):
            selector_checks += 1
            if rows[i][j] != grid_at(p,n,i,j):
                failures.append("selector")
            if ((grid_at(p,n,i,j) == 1) != (i == r and j == c)):
                failures.append("one selector")
            if not grid_at(p,n,i,j) < n*n+1:
                failures.append("range selector")
    neighbor_checks += 1
    if neighbor_summary(p,n,r,c) != direct_neighbor(p,n,r,c):
        failures.append("neighbor summary")

snoc_overlap_checks = 0
finish_checks = 0
odd_bridge_checks = 0
for length in range(0, 9):
    seq = list(range(10, 10+length))
    for value in (-2, 0, 1, 17):
        snoc_overlap_checks += 1
        recursive = seq + [value]
        specialized = seq + [value]
        if recursive != specialized:
            failures.append("snoc overlap")

for prefix_len in range(0, 6):
    a = list(range(prefix_len))
    for pairs in range(0, 12):
        for m in (2, 9):
            pair_prefix = a + [x for _ in range(pairs) for x in (1,m)]
            for parity in (0,1):
                k = 2*pairs + parity
                out = pair_prefix + ([1] if parity else [])
                finish_checks += 1
                computed = a + [x for _ in range(pairs) for x in (1,m)] + ([1] if k % 2 == 1 else [])
                if computed != out:
                    failures.append("finishRel")
            for p in (pair_prefix, pair_prefix + [99], pair_prefix[:-1]):
                odd_bridge_checks += 1
                pair_done = pair_prefix == p
                odd_done = pair_prefix + [1] == p + [1]
                if odd_done != pair_done:
                    failures.append("odd bridge")

print(json.dumps({
    "seed": 12951001,
    "permutation_samples": permutations_checked,
    "selector_lemma_checks": selector_checks,
    "neighbor_summary_checks": neighbor_checks,
    "snoc_overlap_checks": snoc_overlap_checks,
    "finish_relation_checks": finish_checks,
    "odd_bridge_checks": odd_bridge_checks,
    "failures": failures[:20],
    "failure_count": len(failures),
}, indent=2, sort_keys=True))
sys.exit(0 if not failures else 1)
