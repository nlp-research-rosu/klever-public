def get_max_triples(n):
    zero_count = (n + 1) // 3
    one_count = n - zero_count
    zero_triples = zero_count * (zero_count - 1) * (zero_count - 2) // 6
    one_triples = one_count * (one_count - 1) * (one_count - 2) // 6
    return zero_triples + one_triples


# Empty extension and positive-domain branch/count boundaries.
assert get_max_triples(0) == 0
assert get_max_triples(1) == 0
assert get_max_triples(2) == 0
assert get_max_triples(3) == 0
assert get_max_triples(4) == 1
assert get_max_triples(5) == 1
assert get_max_triples(6) == 4
assert get_max_triples(8) == 11

# Normal and larger representative cases cross-checked with canonical Python.
assert get_max_triples(20) == 321
assert get_max_triples(201) == 439989
