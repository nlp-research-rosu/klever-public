def select_words(s, n):
    result = []
    word = ""
    count = 0
    ch = ""
    for ch in s:
        if ch == " ":
            if count == n and word != "":
                result.append(word)
            word = ""
            count = 0
        else:
            word = word + ch
            if ch not in "aeiouAEIOU":
                count = count + 1
    if count == n and word != "":
        result.append(word)
    return result
