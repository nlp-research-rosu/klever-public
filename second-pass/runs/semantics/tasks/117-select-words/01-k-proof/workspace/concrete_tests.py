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


assert select_words("Mary had a little lamb", 4) == ["little"]
assert select_words("Mary had a little lamb", 3) == ["Mary", "lamb"]
assert select_words("simple white space", 2) == []
assert select_words("Hello world", 4) == ["world"]
assert select_words("Uncle sam", 3) == ["Uncle"]
assert select_words("", 0) == []
assert select_words("AEIOU xyz", 0) == ["AEIOU"]
