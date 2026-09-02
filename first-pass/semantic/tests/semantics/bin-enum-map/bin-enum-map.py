assert bin(5) == "0b101"
assert bin(0) == "0b0"
assert bin(12) == "0b1100"

total = 0
for pair in enumerate([10, 20, 30]):
    total = total + pair[0] * pair[1]
assert total == 80

for i, v in enumerate([5, 6]):
    total = total + i + v
assert total == 92

assert map(str, [1, 22, 3]) is not None
ss = map(str, [1, 22])
joined = "-".join(list(ss))
assert joined == "1-22"

c = 0
c += (1 == 1)
c += (1 == 2)
assert c == 1
assert int(7) == 7
