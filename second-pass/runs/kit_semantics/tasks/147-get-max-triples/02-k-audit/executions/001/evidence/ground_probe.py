def get_max_triples(n):
    divisible_by_three = (n + 1) // 3
    not_divisible_by_three = n - divisible_by_three

    triples_of_divisible = (
        divisible_by_three
        * (divisible_by_three - 1)
        * (divisible_by_three - 2)
        // 6
    )
    triples_of_non_divisible = (
        not_divisible_by_three
        * (not_divisible_by_three - 1)
        * (not_divisible_by_three - 2)
        // 6
    )
    return triples_of_divisible + triples_of_non_divisible


result_1 = get_max_triples(1)
result_4 = get_max_triples(4)
result_5 = get_max_triples(5)
result_10 = get_max_triples(10)
result_120 = get_max_triples(120)
