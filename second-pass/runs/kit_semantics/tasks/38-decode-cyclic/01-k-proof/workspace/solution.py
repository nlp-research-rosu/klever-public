def decode_cyclic(s: str):
    """
    Takes a string encoded by rotating each complete three-character group
    left once, and restores the original string.
    """
    result = ""
    group = ""
    char = ""
    for char in s:
        group = group + char
        if len(group) == 3:
            result = result + (group[2] + group[:2])
            group = ""
    return result + group
