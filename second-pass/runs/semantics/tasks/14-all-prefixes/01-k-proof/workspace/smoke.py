def all_prefixes(string):
    prefixes = []
    for end in range(1, len(string) + 1):
        prefixes.append(string[:end])
    return prefixes


assert all_prefixes("") == []
assert all_prefixes("a") == ["a"]
assert all_prefixes("abc") == ["a", "ab", "abc"]
