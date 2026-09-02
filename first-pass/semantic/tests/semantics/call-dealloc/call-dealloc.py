def g(y):
    return y + 1


def f(x):
    t = g(x)
    return t + g(t)


total = 0
i = 0
for i in range(5):
    total = total + f(i)
assert total == 35
