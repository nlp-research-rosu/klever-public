xs = [3, 1, 2]
assert sorted(xs, key=lambda x: -x) == [3, 2, 1]
assert sorted(xs, reverse=True) == [3, 2, 1]
assert sorted(xs, key=lambda x: x) == [1, 2, 3]
ws = ["bbb", "a", "cc"]
assert sorted(ws, key=len) == ["a", "cc", "bbb"]
assert sorted(ws, key=len, reverse=True) == ["bbb", "cc", "a"]
ps = ["ab", "cd", "aa"]
assert sorted(ps, key=lambda w: w[0]) == ["ab", "aa", "cd"]   # stable on equal keys
n = 2


def keyfn(x):
    return x % n


assert sorted([4, 3, 6, 1], key=keyfn) == [4, 6, 3, 1]
assert "a.b.c".split(sep=".") == ["a", "b", "c"]
