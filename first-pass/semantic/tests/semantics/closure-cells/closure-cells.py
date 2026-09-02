# closure cells: nested defs, returned closures, late binding, shared cells


def make_counter():
    def bump(d):
        return d + 1
    return bump


def make_adder(n):
    def add(x):
        return x + n
    return add


def helper(y):
    return y * 10


def uses_global(x):
    def g(y):
        return helper(y) + x
    return g


def late():
    fs = []
    i = 0
    for i in range(3):
        fs.append(lambda: i)
    return fs[0]() + fs[1]() + fs[2]()


def shared_pair():
    v = 7
    def geta():
        return v
    def getb():
        return v + 1
    return geta() + getb()


f = make_counter()
assert f(1) == 2
add3 = make_adder(3)
assert add3(4) == 7
g5 = uses_global(5)
assert g5(2) == 25
assert late() == 6
assert shared_pair() == 15
assert [e for e in [1, 2, 3] if e > 1] == [2, 3]
