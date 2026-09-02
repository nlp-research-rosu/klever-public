def tdiv(a: int, b: int) -> int:
    quotient = abs(a) // abs(b)
    return -quotient if (a < 0) != (b < 0) else quotient


def tmod(a: int, b: int) -> int:
    return a - b * tdiv(a, b)


def py_mod(a: int, b: int) -> int:
    return tmod(tmod(a, b) + b, b)


source_cache = {0: 1, 1: 3}


def source_tri(n: int) -> int:
    if n not in source_cache:
        if n % 2 == 0:
            source_cache[n] = 1 + n // 2
        else:
            source_cache[n] = (
                source_tri(n - 1)
                + source_tri(n - 2)
                + 1
                + (n + 1) // 2
            )
    return source_cache[n]


def candidate_tri(i: int) -> int:
    if py_mod(i, 2) == 0:
        return tdiv(i, 2) + 1
    k = tdiv(i + 1, 2)
    return k * (k + 2)


mismatches = [
    (n, source_tri(n), candidate_tri(n))
    for n in range(10001)
    if source_tri(n) != candidate_tri(n)
]
boundaries = list(range(13)) + [99, 100, 9999, 10000]

print("oracle_domain", "n=0..10000")
print("mismatch_count", len(mismatches))
print("first_mismatches", mismatches[:10])
print("boundary_values", [(n, source_tri(n)) for n in boundaries])
print("constant_mutation_witness", (2, source_tri(2), 0))
print("identity_mutation_witness", (3, source_tri(3), 3))
