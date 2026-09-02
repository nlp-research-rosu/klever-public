def anti_shuffle(s):
    result = ""
    word = ""
    for word in s.split(" "):
        result += "".join(sorted(list(word)))
        result += "!"
    return result[:-1]


assert anti_shuffle("ba a") == "ab!a"
