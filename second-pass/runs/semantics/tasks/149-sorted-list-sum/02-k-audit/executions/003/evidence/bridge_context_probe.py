def sorted_list_sum(lst):
    even_words = []
    for word in lst:
        if len(word) % 2 == 0:
            even_words.append(word)
    # This continuation observes the loop-target binding that Python for-loops
    # leave in the local scope after a nonempty iteration.
    return word


assert sorted_list_sum(["aa"]) == "aa"
