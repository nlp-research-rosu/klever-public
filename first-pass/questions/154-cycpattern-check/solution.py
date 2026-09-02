# solution.py — behavior-preserving rewrite of HumanEval/154 cycpattern_check.
# The canonical scans (i, j) and RETURNS True on the first matching window. This
# rewrite folds a Bool accumulator `found` over the same (i, j) scan instead of
# returning early: found becomes True iff any window a[i:i+l] == pat[j:j+l], which
# is the same result (the early return only short-circuits). Removing the early
# return makes both loops pure Bool-accumulator folds (the is_prime primeAcc rung,
# nested), so there is no frame-pop and no competing FOUND/NOT-FOUND loop claims.
# (`i = 0`, `j = 0` are pre-bound so the loop-var scope shape is stable from
# iteration 0 — the is_prime `k = 0` pattern.)
def cycpattern_check(a, b):
    l = len(b)
    pat = b + b
    found = False
    i = 0
    j = 0
    for i in range(len(a) - l + 1):
        for j in range(l + 1):
            if a[i:i+l] == pat[j:j+l]:
                found = True
    return found
