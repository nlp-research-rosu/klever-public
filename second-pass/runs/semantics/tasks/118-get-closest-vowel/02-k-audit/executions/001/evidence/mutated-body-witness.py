def get_closest_vowel(word):
    if len(word) < 3:
        return "a"  # Deliberate body-sensitivity mutation: original was "".
    result = get_closest_vowel(word[1:])
    if result:
        return result
    if (
        word[1] in "AEIOUaeiou"
        and word[0] not in "AEIOUaeiou"
        and word[2] not in "AEIOUaeiou"
    ):
        return word[1]
    return ""


# A real execution reaches the mutated base case and propagates "a" outward.
assert get_closest_vowel("bbb") == "a"
