def find_max(words):
    best = ""
    best_count = -1
    for word in words:
        count = len(set(word))
        if count > best_count:
            best = word
            best_count = count
        if count == best_count:
            if word < best:
                best = word
    return best
