def words_string(s):
    result = []
    current = ""
    has = False
    ch = ""
    for ch in s + " ":
        if ch in ", ":
            if has:
                result = result + [current]
                current = ""
                has = False
        else:
            current = current + ch
            has = True
    return result


# Smoke checks from the prompt docstring (NOT hidden tests).
assert words_string("Hi, my name is John") == ["Hi", "my", "name", "is", "John"]
assert words_string("One, two, three") == ["One", "two", "three"]
assert words_string("") == []
assert words_string("a") == ["a"]
