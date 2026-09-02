def monotonic(l: list):
    """Return whether l is monotonically nondecreasing or nonincreasing."""
    return l == sorted(l) or l == sorted(l, reverse=True)
