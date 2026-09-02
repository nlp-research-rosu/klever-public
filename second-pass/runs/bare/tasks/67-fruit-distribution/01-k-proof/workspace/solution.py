def fruit_distribution(s, n):
    words = s.split()
    return n - int(words[0]) - int(words[3])
