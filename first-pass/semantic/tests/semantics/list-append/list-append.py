result = []
i = 0
for i in range(5):
    result.append(i * i)
assert result == [0, 1, 4, 9, 16]

xs = [3, 1, 2]
xs.sort()
assert xs == [1, 2, 3]

ys = [0, 0, 0]
j = 0
for j in range(3):
    ys[j] = j + 1
assert ys == [1, 2, 3]
assert ys[-1] == 3

zs = [10]
zs.append(sum(result))
assert zs == [10, 30]
assert len(zs) == 2
