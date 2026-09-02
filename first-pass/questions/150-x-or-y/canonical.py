# canonical.py — the UNMODIFIED HumanEval/150 reference solution (from the dataset).
# Co-located with solution.py (the proof rewrite) to make the original<->rewrite link
# explicit & auditable.  entry point: x_or_y


def x_or_y(n, x, y):
    """A simple program which should return the value of x if n is 
    a prime number and should return the value of y otherwise.

    Examples:
    for x_or_y(7, 34, 12) == 34
    for x_or_y(15, 8, 5) == 5
    
    """
    if n == 1:
        return y
    for i in range(2, n):
        if n % i == 0:
            return y
            break
    else:
        return x
