def do_algebra(operator, operand):
    ops = operator
    nds = operand
    m = len(ops)
    r_ops = []
    r_nds = []
    cur = nds[m] * 1
    k = 0
    i = 0
    base = 0
    for k in range(m):
        i = m - 1 - k
        if ops[i] == '**':
            base = nds[i] * 1
            cur = base ** cur
        else:
            r_nds.append(cur)
            r_ops.append(ops[i])
            cur = nds[i] * 1
    r_nds.append(cur)
    ops = r_ops[::-1]
    nds = r_nds[::-1]
    total = 0
    term = nds[0] * 1
    sign = 1
    o = 0
    for i in range(len(ops)):
        o = ops[i]
        if o == '*':
            term = term * nds[i + 1]
        elif o == '//':
            term = term // nds[i + 1]
        elif o == '+':
            total = total + sign * term
            term = nds[i + 1] * 1
            sign = 1
        else:
            total = total + sign * term
            term = nds[i + 1] * 1
            sign = 0 - 1
    return total + sign * term


# Smoke checks (prompt docstring + precedence cases; NOT hidden tests).
assert do_algebra(["+", "*", "-"], [2, 3, 4, 5]) == 9
assert do_algebra(["**", "*"], [2, 3, 4]) == 32
assert do_algebra(["-", "//"], [10, 3, 2]) == 9
