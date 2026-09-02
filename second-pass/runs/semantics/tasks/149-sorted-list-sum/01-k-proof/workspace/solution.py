def sorted_list_sum(lst):
    even_words = []
    for word in lst:
        if len(word) % 2 == 0:
            even_words.append(word)
    return sorted(sorted(even_words), key=len)
