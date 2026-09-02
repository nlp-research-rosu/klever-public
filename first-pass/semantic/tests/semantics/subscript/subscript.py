# Subscript obj[i] on list / tuple / str. Negative indices count from the end;
# the in-range boundaries (i = 0, len-1, -1, -len) are the easy-to-break cases.
a = [10, 20, 30, 40, 50]
assert a[0] == 10
assert a[4] == 50          # last, positive
assert a[-1] == 50         # last, negative
assert a[-5] == 10         # first, negative (i == -len)
assert a[-2] == 40

s = "hello"
assert s[0] == "h"
assert s[4] == "o"
assert s[-1] == "o"
assert s[-5] == "h"

t = (1, 2, 3)
assert t[0] == 1
assert t[2] == 3
assert t[-1] == 3
assert t[-3] == 1

# index by a computed expression
i = 1
assert a[i + 1] == 30

# singleton boundaries
assert [9][0] == 9
assert [9][-1] == 9
