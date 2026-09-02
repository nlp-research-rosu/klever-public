def reverse_delete(s, c):
    result = ""
    reversed_result = ""
    character = ""
    for character in s:
        if character not in c:
            result += character
            reversed_result = character + reversed_result
    return (result, result == reversed_result)
