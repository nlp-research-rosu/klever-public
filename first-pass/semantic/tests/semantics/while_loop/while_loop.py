# While: the condition is re-checked each iteration. Covers a counting loop, a
# `while True` exited by an early return (the <ret> model unwinds the loop), and a
# loop whose condition is false on entry (body never runs).
i = 0
total = 0
while i < 5:
    total = total + i
    i = i + 1
assert total == 10
assert i == 5


def first_ge(n):
    k = 0
    while True:
        if k * k >= n:
            return k
        k = k + 1


assert first_ge(10) == 4
assert first_ge(0) == 0

j = 0
while j > 0:
    j = j - 1
assert j == 0
