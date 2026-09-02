# break / continue in for & while; nesting (break exits only the inner loop); and the
# interaction with return (the loop stack is reset per call and restored on return).
r = 0
for x in [1, 2, 3, 4]:
    if x == 3:
        break
    r = r + x
assert r == 3

s = 0
for y in [1, 2, 3, 4]:
    if y == 2:
        continue
    s = s + y
assert s == 8

i = 0
t = 0
while True:
    if i >= 3:
        break
    t = t + i
    i = i + 1
assert t == 3

j = 0
u = 0
while j < 5:
    j = j + 1
    if j == 3:
        continue
    u = u + j
assert u == 12

# nested: break exits only the inner loop
cnt = 0
for a in [1, 2]:
    for b in [1, 2, 3]:
        if b == 2:
            break
        cnt = cnt + 1
assert cnt == 2

# break + return frame interaction
def f(xs):
    total = 0
    for x in xs:
        if x < 0:
            break
        total = total + x
    return total


assert f([1, 2, -1, 5]) == 3
assert f([1, 2, 3]) == 6

# return from inside nested loops (loop stack reset/restored across the call)
def first_pair(xs, target):
    for a in xs:
        for b in xs:
            if a + b == target:
                return a * 100 + b
    return -1


assert first_pair([1, 2, 3], 5) == 203
