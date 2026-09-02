# canonical.py — the UNMODIFIED HumanEval/158 reference solution (from the dataset).
# Co-located with solution.py (the proof rewrite) to make the original<->rewrite link
# explicit & auditable.  entry point: find_max


def find_max(words):
    """Write a function that accepts a list of strings.
    The list contains different words. Return the word with maximum number
    of unique characters. If multiple strings have maximum number of unique
    characters, return the one which comes first in lexicographical order.

    find_max(["name", "of", "string"]) == "string"
    find_max(["name", "enam", "game"]) == "enam"
    find_max(["aaaaaaa", "bb" ,"cc"]) == ""aaaaaaa"
    """
    return sorted(words, key = lambda x: (-len(set(x)), x))[0]
