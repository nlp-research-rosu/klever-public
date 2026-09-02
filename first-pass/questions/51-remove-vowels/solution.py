def remove_vowels(text):
    result = ""
    s = ""
    code = 0
    for s in text:
        code = ord(s)
        if code != 97 and code != 101 and code != 105 and code != 111 and code != 117 and code != 65 and code != 69 and code != 73 and code != 79 and code != 85:
            result = result + s
    return result
