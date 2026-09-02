def reverse_delete(s, c):
    result = ""
    reversed_result = ""
    ch = ""
    for ch in s:
        if ch not in c:
            result += ch
            reversed_result = ch + reversed_result
    return (result, result == reversed_result)
