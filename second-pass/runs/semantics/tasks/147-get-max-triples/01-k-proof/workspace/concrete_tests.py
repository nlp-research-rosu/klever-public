def get_max_triples(n):
    zero_count = (n + 1) // 3
    one_count = n - zero_count
    zero_triples = zero_count * (zero_count - 1) * (zero_count - 2) // 6
    one_triples = one_count * (one_count - 1) * (one_count - 2) // 6
    return zero_triples + one_triples


assert get_max_triples(1) == 0
assert get_max_triples(3) == 0
assert get_max_triples(4) == 1
assert get_max_triples(5) == 1
assert get_max_triples(8) == 11
assert get_max_triples(20) == 321
