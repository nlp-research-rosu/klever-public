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


assert select_words("Mary had a little lamb", 4) == ["little"]
assert select_words("Mary had a little lamb", 3) == ["Mary", "lamb"]
assert select_words("simple white space", 2) == []
assert select_words("Hello world", 4) == ["world"]
assert select_words("Uncle sam", 3) == ["Uncle"]
assert select_words("", 0) == []
assert select_words("   ", 0) == []
assert select_words("aeiou AEIOU", 0) == ["aeiou", "AEIOU"]
assert select_words(" b  a c ", 0) == ["a"]
assert select_words(" b  a c ", 1) == ["b", "c"]
assert select_words("abc", 2) == ["abc"]
assert select_words("abc ", 2) == ["abc"]
