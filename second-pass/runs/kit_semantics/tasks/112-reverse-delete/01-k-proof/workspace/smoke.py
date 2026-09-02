def reverse_delete(s, c):
    result = ""
    reversed_result = ""
    ch = ""
    for ch in s:
        if ch not in c:
            result += ch
            reversed_result = ch + reversed_result
    return (result, result == reversed_result)


assert reverse_delete("abcde", "ae") == ("bcd", False)
assert reverse_delete("abcdef", "b") == ("acdef", False)
assert reverse_delete("abcdedcba", "ab") == ("cdedc", True)
assert reverse_delete("", "abc") == ("", True)
assert reverse_delete("abba", "x") == ("abba", True)
