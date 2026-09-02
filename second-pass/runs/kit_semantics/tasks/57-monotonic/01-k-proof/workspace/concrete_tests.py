def monotonic(l: list):
    return l == sorted(l) or l == sorted(l, reverse=True)


assert monotonic([]) == True
assert monotonic([7]) == True
assert monotonic([1, 2, 4, 20]) == True
assert monotonic([1, 20, 4, 10]) == False
assert monotonic([4, 1, 0, -10]) == True
assert monotonic([1, 1, 2, 2]) == True
assert monotonic([2, 2, 1, 1]) == True
