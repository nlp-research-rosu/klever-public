def get_max_triples(n):
    zero_count = (n + 1) // 3
    one_count = n - zero_count
    zero_triples = zero_count * (zero_count - 1) * (zero_count - 2) // 6
    one_triples = one_count * (one_count - 1) * (one_count - 2) // 6
    return zero_triples + one_triples
