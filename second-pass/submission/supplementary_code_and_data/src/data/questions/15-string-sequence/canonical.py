# canonical.py — the UNMODIFIED HumanEval/15 reference solution (from the dataset).
# Co-located with solution.py (the proof rewrite) to make the original<->rewrite link
# explicit & auditable.  entry point: string_sequence



def string_sequence(n: int) -> str:
    """ Return a string containing space-delimited numbers starting from 0 upto n inclusive.
    >>> string_sequence(0)
    '0'
    >>> string_sequence(5)
    '0 1 2 3 4 5'
    """
    return ' '.join([str(x) for x in range(n + 1)])
