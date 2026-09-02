def select_words(s, n):
    result = []
    for word in s.split():
        lower = word.lower()
        consonants = (
            len(word)
            - lower.count("a")
            - lower.count("e")
            - lower.count("i")
            - lower.count("o")
            - lower.count("u")
        )
        if consonants == n:
            result.append(word)
    return result


assert select_words("", 0) == []
assert select_words("     ", 0) == []
assert select_words("AEIOU", 0) == ["AEIOU"]
assert select_words("b", 0) == []
assert select_words("b", 1) == ["b"]
assert select_words("b", 2) == []
assert select_words("a b  c   de", 0) == ["a"]
assert select_words("a b  c   de", 1) == ["b", "c", "de"]
assert select_words("UPPER lower MiXeD", 3) == ["UPPER", "lower", "MiXeD"]
