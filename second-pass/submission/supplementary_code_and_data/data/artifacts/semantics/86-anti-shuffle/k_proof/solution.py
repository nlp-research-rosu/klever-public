def anti_shuffle(s):
    result = ""
    word = ""
    for word in s.split(" "):
        result += "".join(sorted(list(word)))
        result += " "
    return result[:-1]
