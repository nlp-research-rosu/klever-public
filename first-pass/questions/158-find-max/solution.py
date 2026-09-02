def find_max(words):
    best = words[0]
    best_d = len(set(words[0]))
    w = ""
    d = 0
    beats = False
    for w in words:
        d = len(set(w))
        beats = d > best_d or (d == best_d and w < best)
        best = w if beats else best
        best_d = d if beats else best_d
    return best
