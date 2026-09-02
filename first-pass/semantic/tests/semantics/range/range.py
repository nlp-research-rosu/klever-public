# range(stop)
total = 0
for i in range(4):
    total += i
assert total == 6          # 0+1+2+3

# range(start, stop)
t2 = 0
for i in range(2, 5):
    t2 += i
assert t2 == 9             # 2+3+4

# range(start, stop, step)
t3 = 0
for i in range(0, 10, 2):
    t3 += i
assert t3 == 20            # 0+2+4+6+8

# negative step
t4 = 0
for i in range(5, 0, -1):
    t4 += i
assert t4 == 15            # 5+4+3+2+1

# empty range
t5 = 0
for i in range(3, 3):
    t5 += i
assert t5 == 0

# materialised list consumed by other builtins
assert sum(range(4)) == 6
assert len(range(4)) == 4
