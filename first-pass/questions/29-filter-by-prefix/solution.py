def filter_by_prefix(strings, prefix):
    result = []
    x = ""
    for x in strings:
        if x.startswith(prefix):
            result = result + [x]
    return result
