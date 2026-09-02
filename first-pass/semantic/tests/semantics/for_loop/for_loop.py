# For over a list literal (ListExpr), including the empty list (body never runs).
total = 0
for x in [1, 2, 3, 4]:
    total += x
assert total == 10
count = 0
for x in []:
    count += 1
assert count == 0
