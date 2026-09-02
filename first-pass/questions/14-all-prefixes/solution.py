def all_prefixes(string):
    result = []
    acc = ""
    c = ""
    for c in string:
        acc = acc + c
        result = result + [acc]
    return result
