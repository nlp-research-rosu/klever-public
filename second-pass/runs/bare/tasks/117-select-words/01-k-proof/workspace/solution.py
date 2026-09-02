def select_words(s, n):
    """Return, in input order, words containing exactly n consonants."""
    return [
        word
        for word in s.split()
        if len(
            [
                letter
                for letter in word
                if letter.lower() not in "aeiou"
            ]
        )
        == n
    ]
