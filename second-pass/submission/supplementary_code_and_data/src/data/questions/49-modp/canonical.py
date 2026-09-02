# canonical.py — the UNMODIFIED HumanEval/49 reference solution (from the dataset).
# Co-located with solution.py (the proof rewrite) to make the original<->rewrite link
# explicit & auditable.  entry point: modp



def modp(n: int, p: int):
    """Return 2^n modulo p (be aware of numerics).
    >>> modp(3, 5)
    3
    >>> modp(1101, 101)
    2
    >>> modp(0, 101)
    1
    >>> modp(3, 11)
    8
    >>> modp(100, 101)
    1
    """
    ret = 1
    for i in range(n):
        ret = (2 * ret) % p
    return ret
