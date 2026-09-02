# solution.py — behavior-preserving rewrite of HumanEval/160 do_algebra (no eval, no trusted call).
# The canonical builds a string and eval()s it with Python precedence. This rewrite evaluates the
# (operator, operand) lists directly via TWO passes: (1) ** RIGHT-associative (right-to-left, reduces
# the operator/operand lists via `+ [x]`); (2) a COMBINED * // + - pass that folds SCALAR accumulators
# (total, term, sign) with NO further list building — * // multiply/floor-div into `term`, and + -
# flush `sign*term` into `total` (sign applied AFTER term is finalized, so floor-division sign is
# correct). Diff-tested vs canonical/eval over the whole documented domain.
def do_algebra(operator, operand):
    ops = operator
    nds = operand
    m = len(ops)
    # ---- pass 1: ** (RIGHT-associative): scan right-to-left, fold ** chains into `cur`; emit the
    # non-** operators/operands into reversed output lists via in-place .append(), then reverse.
    # (.append mutates the same list object -> a stable heap ref, which the proof needs; `* 1` keeps
    # cur/base scalar ints.)
    r_ops = []
    r_nds = []
    cur = nds[m] * 1
    k = 0  # pre-declare loop-body vars so they exist from iteration 0 (proof scope determinism)
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
    # ---- pass 2: combined * // + - (SCALAR accumulators, no list building). `term` is the current
    # multiplicative run; `total` accumulates finalized signed terms; `sign` is +1/-1 for the term.
    total = 0
    term = nds[0] * 1
    sign = 1
    o = 0  # pre-declare the combined-loop var
    for i in range(len(ops)):
        o = ops[i]
        if o == '*':
            term = term * nds[i + 1]
        elif o == '//':
            term = term // nds[i + 1]
        elif o == '+':
            total = total + sign * term
            term = nds[i + 1] * 1  # * 1 keeps `term` a scalar int (fresh multiplicative run)
            sign = 1
        else:
            total = total + sign * term
            term = nds[i + 1] * 1
            sign = 0 - 1
    return total + sign * term
