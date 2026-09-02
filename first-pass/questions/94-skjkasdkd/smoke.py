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


# Smoke checks — the HumanEval/94 dataset `check` cases (bare-value asserts).
assert skjkasdkd([0, 81, 12, 3, 1, 21]) == 3
assert skjkasdkd([0, 8, 1, 2, 1, 7]) == 7
assert skjkasdkd([2, 3, 5]) == 5
assert skjkasdkd([1, 0, 4]) == 1
