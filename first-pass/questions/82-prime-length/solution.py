def prime_length(string):
    l = len(string)
    prime = l >= 2
    i = 0
    for i in range(2, l):
        if l % i == 0:
            prime = False
    return prime
