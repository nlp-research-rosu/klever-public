def reverse_delete(s, c):
    result = ""
    reversed_result = ""
    character = ""
    for character in s:
        if character not in c:
            result += character
            reversed_result = character + reversed_result
    return (result, result == reversed_result)


# Documented examples.
assert reverse_delete("abcde", "ae") == ("bcd", False)
assert reverse_delete("abcdef", "b") == ("acdef", False)
assert reverse_delete("abcdedcba", "ab") == ("cdedc", True)

# Empty, branch-boundary, and representative cases supported by MPY strings.
assert reverse_delete("", "") == ("", True)
assert reverse_delete("", "anything") == ("", True)
assert reverse_delete("x", "") == ("x", True)
assert reverse_delete("x", "x") == ("", True)
assert reverse_delete("abc", "abc") == ("", True)
assert reverse_delete("abba", "") == ("abba", True)
assert reverse_delete("abc", "") == ("abc", False)
assert reverse_delete("ababab", "b") == ("aaa", True)
