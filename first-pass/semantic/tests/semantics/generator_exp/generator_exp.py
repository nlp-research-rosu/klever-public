# Generator expressions consumed by an aggregator (sum / all / any / max).
assert sum(x for x in [1, 2, 3]) == 6
assert sum(x * x for x in [1, 2, 3]) == 14
assert sum(x > 0 for x in [1, -1, 2, -3]) == 2      # sum of bools counts the Trues
assert sum(i for i in range(5)) == 10
assert all(x > 0 for x in [1, 2, 3])
assert not all(x > 0 for x in [1, -1, 3])
assert any(x < 0 for x in [1, -1, 3])
assert not any(x < 0 for x in [1, 2, 3])
assert max(x for x in [3, 1, 4, 1, 5]) == 5
