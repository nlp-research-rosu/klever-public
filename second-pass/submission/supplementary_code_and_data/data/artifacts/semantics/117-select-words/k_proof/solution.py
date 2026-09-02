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
