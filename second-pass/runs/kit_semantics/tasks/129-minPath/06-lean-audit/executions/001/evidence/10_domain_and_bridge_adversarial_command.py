from itertools import permutations, product
import importlib.util


def p_at_total(p, i):
    return p[i] if 0 <= i < len(p) else 0


def grid_at(p, n, i, j):
    return p_at_total(p, i * n + j)


def grid_row(p, n, i):
    return [grid_at(p, n, i, j) for j in range(max(n, 0))]


def grid_rows(p, n):
    return [grid_row(p, n, i) for i in range(max(n, 0))]


def valid_perm_k(p, m):
    return len(p) == m and all(1 <= x <= m for x in p) and len(set(p)) == len(p)


def valid_perm_candidate(p, m):
    return m >= 0 and sorted(p) == list(range(1, m + 1))


def find_one(p, a=0):
    for i, x in enumerate(p):
        if x == 1:
            return a + i
    return -1


def one_row_k(p, n):
    return int(find_one(p) / n) if n > 0 else 0  # K /Int truncates toward zero


def py_mod(i, n):
    return 0 if n == 0 else ((i % abs(n)) + n) % abs(n)


def one_col_k(p, n):
    return py_mod(find_one(p), n) if n > 0 else 0


def snoc(a, v):
    return a + [v]


def pair_prefix(a, m, r):
    out = list(a)
    while r > 0:
        out = snoc(snoc(out, 1), m)
        r -= 1
    return out


def pair_done(a, o, r, m):
    return pair_prefix(a, m, max(r, 0)) == o


def odd_done(a, o, r, m):
    return o == snoc(pair_prefix(a, m, max(r, 0)), 1)


lemma_checks = [0] * 7
for n in (2, 3):
    # N=2 is exhaustive; N=3 uses deliberately diverse permutations to avoid a 9! audit loop.
    values = list(range(1, n * n + 1))
    ps = list(permutations(values)) if n == 2 else [
        tuple(values), tuple(reversed(values)),
        (9, 1, 8, 2, 7, 3, 6, 4, 5),
        (2, 3, 4, 5, 6, 7, 8, 9, 1),
    ]
    for p in ps:
        assert valid_perm_k(p, n*n)
        assert valid_perm_candidate(p, n*n)
        rows = grid_rows(p, n)
        assert len(rows) == n
        lemma_checks[0] += 1
        for i in range(n):
            assert rows[i] == grid_row(p, n, i)
            lemma_checks[1] += 1
            for j in range(n):
                assert rows[i][j] == grid_at(p, n, i, j)
                lemma_checks[2] += 1
                assert (grid_at(p, n, i, j) == 1) == (i == one_row_k(p, n) and j == one_col_k(p, n))
                lemma_checks[3] += 1
                assert grid_at(p, n, i, j) < n*n + 1
                lemma_checks[4] += 1

seqs = [[]]
for length in range(1, 5):
    seqs.extend(map(list, product((-1, 0, 1, 7), repeat=length)))
for a in seqs:
    for v in (-2, 0, 1, 9):
        assert a + [v] == snoc(a, v)
        lemma_checks[5] += 1

short = [[]]
for length in range(1, 4):
    short.extend(map(list, product((0, 1, 5), repeat=length)))
for a in short:
    for p in short:
        for m in (-3, 0, 1, 8):
            for r in range(0, 7):
                assert odd_done(a, snoc(p, 1), r, m) == pair_done(a, p, r, m)
                lemma_checks[6] += 1

adversarial = [
    ([], -2), ([], 0), ([1], 1), ([1, 1], 2), ([0, 1], 2),
    ([2, 1], 2), ([1, 2, 3, 4], 4), ([4, 2, 1, 3], 4),
]
for p, m in adversarial:
    assert valid_perm_k(p, m) == valid_perm_candidate(p, m)

# Concrete counterexamples show why convenient bridge mutations are unsound.
p = [1, 2, 3, 4]
mutation_counterexamples = {
    "gridAt_constant_zero": ((grid_at(p, 2, 0, 0) == 1), (0 == 1)),
    "gridAt_constant_one": ((grid_at(p, 2, 0, 1) == 1), (1 == 1)),
    "valSeqConcat_identity": (([] + [7]), []),
    "snoc_identity": (snoc([], 1), []),
    "validPerm_constant_false_vacuates_first_five": (valid_perm_k(p, 4), False),
    "odd_pair_both_constant_false_vacuates_seventh": (
        odd_done([], [1], 0, 5) == pair_done([], [], 0, 5),
        False == False,
    ),
}
assert mutation_counterexamples["gridAt_constant_zero"][0] != mutation_counterexamples["gridAt_constant_zero"][1]
assert mutation_counterexamples["gridAt_constant_one"][0] != mutation_counterexamples["gridAt_constant_one"][1]
assert mutation_counterexamples["valSeqConcat_identity"][0] != mutation_counterexamples["valSeqConcat_identity"][1]
assert mutation_counterexamples["snoc_identity"][0] != mutation_counterexamples["snoc_identity"][1]

# Execute frozen source on edge-position and parity cases and compare exact intended result.
spec = importlib.util.spec_from_file_location("frozen_solution", "/reference/k-proof/solution.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
source_cases = [
    ([[1, 2], [3, 4]], 1),
    ([[1, 2], [3, 4]], 6),
    ([[2, 3], [4, 1]], 5),
    ([[4, 1], [3, 2]], 4),
    ([[2, 5, 9], [8, 1, 6], [7, 3, 4]], 7),
]
source_results = []
for grid, k in source_cases:
    n = len(grid)
    pos = next((i, j) for i in range(n) for j in range(n) if grid[i][j] == 1)
    i, j = pos
    neighbors = []
    if i > 0: neighbors.append(grid[i-1][j])
    if i+1 < n: neighbors.append(grid[i+1][j])
    if j > 0: neighbors.append(grid[i][j-1])
    if j+1 < n: neighbors.append(grid[i][j+1])
    expected = ([1, min(neighbors)] * (k // 2)) + ([1] if k % 2 else [])
    actual = module.minPath(grid, k)
    assert actual == expected
    source_results.append((grid, k, actual))

print("domain_lemma_successful_case_counts", lemma_checks)
print("validPerm_K_vs_candidate_adversarial_count", len(adversarial), "mismatches=0")
print("operational_bridge_mutation_counterexamples", mutation_counterexamples)
print("frozen_source_adversarial_results", source_results)
print("RESULT PASS")
