def reverse_delete(s, c):
    result = ""
    reversed_result = ""
    character = ""
    for character in s:
        if character not in c:
            result += character
            reversed_result = character + reversed_result
    return (result, result == reversed_result)


assert reverse_delete("abcde", "ae") == ("bcd", False)
assert reverse_delete("abcdef", "b") == ("acdef", False)
assert reverse_delete("abcdedcba", "ab") == ("cdedc", True)
assert reverse_delete("", "anything") == ("", True)
assert reverse_delete("abba", "") == ("abba", True)
assert reverse_delete("abc", "abc") == ("", True)
