def skjkasdkd(lst):
    def isPrime(n):
        p = True
        for i in range(2, int(n**0.5)+1):
            if n % i == 0:
                p = False
        return p
    maxx = 0
    i = 0
    while i < len(lst):
        if(lst[i] > maxx and isPrime(lst[i])):
            maxx = lst[i]
        i += 1
    result = 0
    for digit in str(maxx):
        result = result + int(digit)
    return result
