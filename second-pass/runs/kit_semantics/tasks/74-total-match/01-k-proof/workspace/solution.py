def _total_length(strings):
    total = 0
    string = None
    for string in strings:
        total += len(string)
    return total


def total_match(lst1, lst2):
    if _total_length(lst1) <= _total_length(lst2):
        return lst1
    return lst2
