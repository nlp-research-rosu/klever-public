def all_prefixes(string):
    prefixes = []
    prefix = ""
    char = ""
    for char in string:
        prefix = prefix + char
        prefixes.append(prefix)
    return prefixes


empty_result = all_prefixes("")
abc_result = all_prefixes("abc")
