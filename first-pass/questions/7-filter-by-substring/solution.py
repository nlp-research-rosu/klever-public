def filter_by_substring(strings, substring):
    result = []
    x = ""
    for x in strings:
        if substring in x:
            result = result + [x]
    return result
