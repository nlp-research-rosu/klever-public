d = {"a": 1, "b": 2}
assert d["a"] == 1
assert d["b"] == 2
d["c"] = 3
assert d["c"] == 3
n = {1: "one", 2: "two"}
assert n[2] == "two"
xs = []
xs.append(d["a"])
assert xs == [1]
