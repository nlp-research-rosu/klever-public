def unique(l: list):
    """Return sorted unique elements in a list."""
    result = []
    x = None
    for x in l:
        if x not in result:
            result.append(x)
    return sorted(result)


answer = unique([True, 1])

