def _has_pair_sum(first: int, rest: list):
    if not rest:
        return False
    if 0 - first - rest[0] in rest[1:]:
        return True
    return _has_pair_sum(first, rest[1:])


def triples_sum_to_zero(l: list):
    if not l:
        return False
    if _has_pair_sum(l[0], l[1:]):
        return True
    return triples_sum_to_zero(l[1:])
