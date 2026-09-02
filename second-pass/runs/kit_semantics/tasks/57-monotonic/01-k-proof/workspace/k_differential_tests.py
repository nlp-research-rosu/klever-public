def monotonic(l: list):
    return l == sorted(l) or l == sorted(l, reverse=True)

assert monotonic([]) == True
assert monotonic([-2]) == True
assert monotonic([-1]) == True
assert monotonic([0]) == True
assert monotonic([1]) == True
assert monotonic([2]) == True
assert monotonic([-2, -2]) == True
assert monotonic([-2, -1]) == True
assert monotonic([-2, 0]) == True
assert monotonic([-2, 1]) == True
assert monotonic([-2, 2]) == True
assert monotonic([-1, -2]) == True
assert monotonic([-1, -1]) == True
assert monotonic([-1, 0]) == True
assert monotonic([-1, 1]) == True
assert monotonic([-1, 2]) == True
assert monotonic([0, -2]) == True
assert monotonic([0, -1]) == True
assert monotonic([0, 0]) == True
assert monotonic([0, 1]) == True
assert monotonic([0, 2]) == True
assert monotonic([1, -2]) == True
assert monotonic([1, -1]) == True
assert monotonic([1, 0]) == True
assert monotonic([1, 1]) == True
assert monotonic([1, 2]) == True
assert monotonic([2, -2]) == True
assert monotonic([2, -1]) == True
assert monotonic([2, 0]) == True
assert monotonic([2, 1]) == True
assert monotonic([2, 2]) == True
assert monotonic([-2, -2, -2]) == True
assert monotonic([-2, -2, -1]) == True
assert monotonic([-2, -2, 0]) == True
assert monotonic([-2, -2, 1]) == True
assert monotonic([-2, -2, 2]) == True
assert monotonic([-2, -1, -2]) == False
assert monotonic([-2, -1, -1]) == True
assert monotonic([-2, -1, 0]) == True
assert monotonic([-2, -1, 1]) == True
assert monotonic([-2, -1, 2]) == True
assert monotonic([-2, 0, -2]) == False
assert monotonic([-2, 0, -1]) == False
assert monotonic([-2, 0, 0]) == True
assert monotonic([-2, 0, 1]) == True
assert monotonic([-2, 0, 2]) == True
assert monotonic([-2, 1, -2]) == False
assert monotonic([-2, 1, -1]) == False
assert monotonic([-2, 1, 0]) == False
assert monotonic([-2, 1, 1]) == True
assert monotonic([-2, 1, 2]) == True
assert monotonic([-2, 2, -2]) == False
assert monotonic([-2, 2, -1]) == False
assert monotonic([-2, 2, 0]) == False
assert monotonic([-2, 2, 1]) == False
assert monotonic([-2, 2, 2]) == True
assert monotonic([-1, -2, -2]) == True
assert monotonic([-1, -2, -1]) == False
assert monotonic([-1, -2, 0]) == False
assert monotonic([-1, -2, 1]) == False
assert monotonic([-1, -2, 2]) == False
assert monotonic([-1, -1, -2]) == True
assert monotonic([-1, -1, -1]) == True
assert monotonic([-1, -1, 0]) == True
assert monotonic([-1, -1, 1]) == True
assert monotonic([-1, -1, 2]) == True
assert monotonic([-1, 0, -2]) == False
assert monotonic([-1, 0, -1]) == False
assert monotonic([-1, 0, 0]) == True
assert monotonic([-1, 0, 1]) == True
assert monotonic([-1, 0, 2]) == True
assert monotonic([-1, 1, -2]) == False
assert monotonic([-1, 1, -1]) == False
assert monotonic([-1, 1, 0]) == False
assert monotonic([-1, 1, 1]) == True
assert monotonic([-1, 1, 2]) == True
assert monotonic([-1, 2, -2]) == False
assert monotonic([-1, 2, -1]) == False
assert monotonic([-1, 2, 0]) == False
assert monotonic([-1, 2, 1]) == False
assert monotonic([-1, 2, 2]) == True
assert monotonic([0, -2, -2]) == True
assert monotonic([0, -2, -1]) == False
assert monotonic([0, -2, 0]) == False
assert monotonic([0, -2, 1]) == False
assert monotonic([0, -2, 2]) == False
assert monotonic([0, -1, -2]) == True
assert monotonic([0, -1, -1]) == True
assert monotonic([0, -1, 0]) == False
assert monotonic([0, -1, 1]) == False
assert monotonic([0, -1, 2]) == False
assert monotonic([0, 0, -2]) == True
assert monotonic([0, 0, -1]) == True
assert monotonic([0, 0, 0]) == True
assert monotonic([0, 0, 1]) == True
assert monotonic([0, 0, 2]) == True
assert monotonic([0, 1, -2]) == False
assert monotonic([0, 1, -1]) == False
assert monotonic([0, 1, 0]) == False
assert monotonic([0, 1, 1]) == True
assert monotonic([0, 1, 2]) == True
assert monotonic([0, 2, -2]) == False
assert monotonic([0, 2, -1]) == False
assert monotonic([0, 2, 0]) == False
assert monotonic([0, 2, 1]) == False
assert monotonic([0, 2, 2]) == True
assert monotonic([1, -2, -2]) == True
assert monotonic([1, -2, -1]) == False
assert monotonic([1, -2, 0]) == False
assert monotonic([1, -2, 1]) == False
assert monotonic([1, -2, 2]) == False
assert monotonic([1, -1, -2]) == True
assert monotonic([1, -1, -1]) == True
assert monotonic([1, -1, 0]) == False
assert monotonic([1, -1, 1]) == False
assert monotonic([1, -1, 2]) == False
assert monotonic([1, 0, -2]) == True
assert monotonic([1, 0, -1]) == True
assert monotonic([1, 0, 0]) == True
assert monotonic([1, 0, 1]) == False
assert monotonic([1, 0, 2]) == False
assert monotonic([1, 1, -2]) == True
assert monotonic([1, 1, -1]) == True
assert monotonic([1, 1, 0]) == True
assert monotonic([1, 1, 1]) == True
assert monotonic([1, 1, 2]) == True
assert monotonic([1, 2, -2]) == False
assert monotonic([1, 2, -1]) == False
assert monotonic([1, 2, 0]) == False
assert monotonic([1, 2, 1]) == False
assert monotonic([1, 2, 2]) == True
assert monotonic([2, -2, -2]) == True
assert monotonic([2, -2, -1]) == False
assert monotonic([2, -2, 0]) == False
assert monotonic([2, -2, 1]) == False
assert monotonic([2, -2, 2]) == False
assert monotonic([2, -1, -2]) == True
assert monotonic([2, -1, -1]) == True
assert monotonic([2, -1, 0]) == False
assert monotonic([2, -1, 1]) == False
assert monotonic([2, -1, 2]) == False
assert monotonic([2, 0, -2]) == True
assert monotonic([2, 0, -1]) == True
assert monotonic([2, 0, 0]) == True
assert monotonic([2, 0, 1]) == False
assert monotonic([2, 0, 2]) == False
assert monotonic([2, 1, -2]) == True
assert monotonic([2, 1, -1]) == True
assert monotonic([2, 1, 0]) == True
assert monotonic([2, 1, 1]) == True
assert monotonic([2, 1, 2]) == False
assert monotonic([2, 2, -2]) == True
assert monotonic([2, 2, -1]) == True
assert monotonic([2, 2, 0]) == True
assert monotonic([2, 2, 1]) == True
assert monotonic([2, 2, 2]) == True
assert monotonic([-2, -2, -2, -2]) == True
assert monotonic([-2, -2, -2, -1]) == True
assert monotonic([-2, -2, -2, 0]) == True
assert monotonic([-2, -2, -2, 1]) == True
assert monotonic([-2, -2, -2, 2]) == True
assert monotonic([-2, -2, -1, -2]) == False
assert monotonic([-2, -2, -1, -1]) == True
assert monotonic([-2, -2, -1, 0]) == True
assert monotonic([-2, -2, -1, 1]) == True
assert monotonic([-2, -2, -1, 2]) == True
assert monotonic([-2, -2, 0, -2]) == False
assert monotonic([-2, -2, 0, -1]) == False
assert monotonic([-2, -2, 0, 0]) == True
assert monotonic([-2, -2, 0, 1]) == True
assert monotonic([-2, -2, 0, 2]) == True
assert monotonic([-2, -2, 1, -2]) == False
assert monotonic([-2, -2, 1, -1]) == False
assert monotonic([-2, -2, 1, 0]) == False
assert monotonic([-2, -2, 1, 1]) == True
assert monotonic([-2, -2, 1, 2]) == True
assert monotonic([-2, -2, 2, -2]) == False
assert monotonic([-2, -2, 2, -1]) == False
assert monotonic([-2, -2, 2, 0]) == False
assert monotonic([-2, -2, 2, 1]) == False
assert monotonic([-2, -2, 2, 2]) == True
assert monotonic([-2, -1, -2, -2]) == False
assert monotonic([-2, -1, -2, -1]) == False
assert monotonic([-2, -1, -2, 0]) == False
assert monotonic([-2, -1, -2, 1]) == False
assert monotonic([-2, -1, -2, 2]) == False
assert monotonic([-2, -1, -1, -2]) == False
assert monotonic([-2, -1, -1, -1]) == True
assert monotonic([-2, -1, -1, 0]) == True
assert monotonic([-2, -1, -1, 1]) == True
assert monotonic([-2, -1, -1, 2]) == True
assert monotonic([-2, -1, 0, -2]) == False
assert monotonic([-2, -1, 0, -1]) == False
assert monotonic([-2, -1, 0, 0]) == True
assert monotonic([-2, -1, 0, 1]) == True
assert monotonic([-2, -1, 0, 2]) == True
assert monotonic([-2, -1, 1, -2]) == False
assert monotonic([-2, -1, 1, -1]) == False
assert monotonic([-2, -1, 1, 0]) == False
assert monotonic([-2, -1, 1, 1]) == True
assert monotonic([-2, -1, 1, 2]) == True
assert monotonic([-2, -1, 2, -2]) == False
assert monotonic([-2, -1, 2, -1]) == False
assert monotonic([-2, -1, 2, 0]) == False
assert monotonic([-2, -1, 2, 1]) == False
assert monotonic([-2, -1, 2, 2]) == True
assert monotonic([-2, 0, -2, -2]) == False
assert monotonic([-2, 0, -2, -1]) == False
assert monotonic([-2, 0, -2, 0]) == False
assert monotonic([-2, 0, -2, 1]) == False
assert monotonic([-2, 0, -2, 2]) == False
assert monotonic([-2, 0, -1, -2]) == False
assert monotonic([-2, 0, -1, -1]) == False
assert monotonic([-2, 0, -1, 0]) == False
assert monotonic([-2, 0, -1, 1]) == False
assert monotonic([-2, 0, -1, 2]) == False
assert monotonic([-2, 0, 0, -2]) == False
assert monotonic([-2, 0, 0, -1]) == False
assert monotonic([-2, 0, 0, 0]) == True
assert monotonic([-2, 0, 0, 1]) == True
assert monotonic([-2, 0, 0, 2]) == True
assert monotonic([-2, 0, 1, -2]) == False
assert monotonic([-2, 0, 1, -1]) == False
assert monotonic([-2, 0, 1, 0]) == False
assert monotonic([-2, 0, 1, 1]) == True
assert monotonic([-2, 0, 1, 2]) == True
assert monotonic([-2, 0, 2, -2]) == False
assert monotonic([-2, 0, 2, -1]) == False
assert monotonic([-2, 0, 2, 0]) == False
assert monotonic([-2, 0, 2, 1]) == False
assert monotonic([-2, 0, 2, 2]) == True
assert monotonic([-2, 1, -2, -2]) == False
assert monotonic([-2, 1, -2, -1]) == False
assert monotonic([-2, 1, -2, 0]) == False
assert monotonic([-2, 1, -2, 1]) == False
assert monotonic([-2, 1, -2, 2]) == False
assert monotonic([-2, 1, -1, -2]) == False
assert monotonic([-2, 1, -1, -1]) == False
assert monotonic([-2, 1, -1, 0]) == False
assert monotonic([-2, 1, -1, 1]) == False
assert monotonic([-2, 1, -1, 2]) == False
assert monotonic([-2, 1, 0, -2]) == False
assert monotonic([-2, 1, 0, -1]) == False
assert monotonic([-2, 1, 0, 0]) == False
assert monotonic([-2, 1, 0, 1]) == False
assert monotonic([-2, 1, 0, 2]) == False
assert monotonic([-2, 1, 1, -2]) == False
assert monotonic([-2, 1, 1, -1]) == False
assert monotonic([-2, 1, 1, 0]) == False
assert monotonic([-2, 1, 1, 1]) == True
assert monotonic([-2, 1, 1, 2]) == True
assert monotonic([-2, 1, 2, -2]) == False
assert monotonic([-2, 1, 2, -1]) == False
assert monotonic([-2, 1, 2, 0]) == False
assert monotonic([-2, 1, 2, 1]) == False
assert monotonic([-2, 1, 2, 2]) == True
assert monotonic([-2, 2, -2, -2]) == False
assert monotonic([-2, 2, -2, -1]) == False
assert monotonic([-2, 2, -2, 0]) == False
assert monotonic([-2, 2, -2, 1]) == False
assert monotonic([-2, 2, -2, 2]) == False
assert monotonic([-2, 2, -1, -2]) == False
assert monotonic([-2, 2, -1, -1]) == False
assert monotonic([-2, 2, -1, 0]) == False
assert monotonic([-2, 2, -1, 1]) == False
assert monotonic([-2, 2, -1, 2]) == False
assert monotonic([-2, 2, 0, -2]) == False
assert monotonic([-2, 2, 0, -1]) == False
assert monotonic([-2, 2, 0, 0]) == False
assert monotonic([-2, 2, 0, 1]) == False
assert monotonic([-2, 2, 0, 2]) == False
assert monotonic([-2, 2, 1, -2]) == False
assert monotonic([-2, 2, 1, -1]) == False
assert monotonic([-2, 2, 1, 0]) == False
assert monotonic([-2, 2, 1, 1]) == False
assert monotonic([-2, 2, 1, 2]) == False
assert monotonic([-2, 2, 2, -2]) == False
assert monotonic([-2, 2, 2, -1]) == False
assert monotonic([-2, 2, 2, 0]) == False
assert monotonic([-2, 2, 2, 1]) == False
assert monotonic([-2, 2, 2, 2]) == True
assert monotonic([-1, -2, -2, -2]) == True
assert monotonic([-1, -2, -2, -1]) == False
assert monotonic([-1, -2, -2, 0]) == False
assert monotonic([-1, -2, -2, 1]) == False
assert monotonic([-1, -2, -2, 2]) == False
assert monotonic([-1, -2, -1, -2]) == False
assert monotonic([-1, -2, -1, -1]) == False
assert monotonic([-1, -2, -1, 0]) == False
assert monotonic([-1, -2, -1, 1]) == False
assert monotonic([-1, -2, -1, 2]) == False
assert monotonic([-1, -2, 0, -2]) == False
assert monotonic([-1, -2, 0, -1]) == False
assert monotonic([-1, -2, 0, 0]) == False
assert monotonic([-1, -2, 0, 1]) == False
assert monotonic([-1, -2, 0, 2]) == False
assert monotonic([-1, -2, 1, -2]) == False
assert monotonic([-1, -2, 1, -1]) == False
assert monotonic([-1, -2, 1, 0]) == False
assert monotonic([-1, -2, 1, 1]) == False
assert monotonic([-1, -2, 1, 2]) == False
assert monotonic([-1, -2, 2, -2]) == False
assert monotonic([-1, -2, 2, -1]) == False
assert monotonic([-1, -2, 2, 0]) == False
assert monotonic([-1, -2, 2, 1]) == False
assert monotonic([-1, -2, 2, 2]) == False
assert monotonic([-1, -1, -2, -2]) == True
assert monotonic([-1, -1, -2, -1]) == False
assert monotonic([-1, -1, -2, 0]) == False
assert monotonic([-1, -1, -2, 1]) == False
assert monotonic([-1, -1, -2, 2]) == False
assert monotonic([-1, -1, -1, -2]) == True
assert monotonic([-1, -1, -1, -1]) == True
assert monotonic([-1, -1, -1, 0]) == True
assert monotonic([-1, -1, -1, 1]) == True
assert monotonic([-1, -1, -1, 2]) == True
assert monotonic([-1, -1, 0, -2]) == False
assert monotonic([-1, -1, 0, -1]) == False
assert monotonic([-1, -1, 0, 0]) == True
assert monotonic([-1, -1, 0, 1]) == True
assert monotonic([-1, -1, 0, 2]) == True
assert monotonic([-1, -1, 1, -2]) == False
assert monotonic([-1, -1, 1, -1]) == False
assert monotonic([-1, -1, 1, 0]) == False
assert monotonic([-1, -1, 1, 1]) == True
assert monotonic([-1, -1, 1, 2]) == True
assert monotonic([-1, -1, 2, -2]) == False
assert monotonic([-1, -1, 2, -1]) == False
assert monotonic([-1, -1, 2, 0]) == False
assert monotonic([-1, -1, 2, 1]) == False
assert monotonic([-1, -1, 2, 2]) == True
assert monotonic([-1, 0, -2, -2]) == False
assert monotonic([-1, 0, -2, -1]) == False
assert monotonic([-1, 0, -2, 0]) == False
assert monotonic([-1, 0, -2, 1]) == False
assert monotonic([-1, 0, -2, 2]) == False
assert monotonic([-1, 0, -1, -2]) == False
assert monotonic([-1, 0, -1, -1]) == False
assert monotonic([-1, 0, -1, 0]) == False
assert monotonic([-1, 0, -1, 1]) == False
assert monotonic([-1, 0, -1, 2]) == False
assert monotonic([-1, 0, 0, -2]) == False
assert monotonic([-1, 0, 0, -1]) == False
assert monotonic([-1, 0, 0, 0]) == True
assert monotonic([-1, 0, 0, 1]) == True
assert monotonic([-1, 0, 0, 2]) == True
assert monotonic([-1, 0, 1, -2]) == False
assert monotonic([-1, 0, 1, -1]) == False
assert monotonic([-1, 0, 1, 0]) == False
assert monotonic([-1, 0, 1, 1]) == True
assert monotonic([-1, 0, 1, 2]) == True
assert monotonic([-1, 0, 2, -2]) == False
assert monotonic([-1, 0, 2, -1]) == False
assert monotonic([-1, 0, 2, 0]) == False
assert monotonic([-1, 0, 2, 1]) == False
assert monotonic([-1, 0, 2, 2]) == True
assert monotonic([-1, 1, -2, -2]) == False
assert monotonic([-1, 1, -2, -1]) == False
assert monotonic([-1, 1, -2, 0]) == False
assert monotonic([-1, 1, -2, 1]) == False
assert monotonic([-1, 1, -2, 2]) == False
assert monotonic([-1, 1, -1, -2]) == False
assert monotonic([-1, 1, -1, -1]) == False
assert monotonic([-1, 1, -1, 0]) == False
assert monotonic([-1, 1, -1, 1]) == False
assert monotonic([-1, 1, -1, 2]) == False
assert monotonic([-1, 1, 0, -2]) == False
assert monotonic([-1, 1, 0, -1]) == False
assert monotonic([-1, 1, 0, 0]) == False
assert monotonic([-1, 1, 0, 1]) == False
assert monotonic([-1, 1, 0, 2]) == False
assert monotonic([-1, 1, 1, -2]) == False
assert monotonic([-1, 1, 1, -1]) == False
assert monotonic([-1, 1, 1, 0]) == False
assert monotonic([-1, 1, 1, 1]) == True
assert monotonic([-1, 1, 1, 2]) == True
assert monotonic([-1, 1, 2, -2]) == False
assert monotonic([-1, 1, 2, -1]) == False
assert monotonic([-1, 1, 2, 0]) == False
assert monotonic([-1, 1, 2, 1]) == False
assert monotonic([-1, 1, 2, 2]) == True
assert monotonic([-1, 2, -2, -2]) == False
assert monotonic([-1, 2, -2, -1]) == False
assert monotonic([-1, 2, -2, 0]) == False
assert monotonic([-1, 2, -2, 1]) == False
assert monotonic([-1, 2, -2, 2]) == False
assert monotonic([-1, 2, -1, -2]) == False
assert monotonic([-1, 2, -1, -1]) == False
assert monotonic([-1, 2, -1, 0]) == False
assert monotonic([-1, 2, -1, 1]) == False
assert monotonic([-1, 2, -1, 2]) == False
assert monotonic([-1, 2, 0, -2]) == False
assert monotonic([-1, 2, 0, -1]) == False
assert monotonic([-1, 2, 0, 0]) == False
assert monotonic([-1, 2, 0, 1]) == False
assert monotonic([-1, 2, 0, 2]) == False
assert monotonic([-1, 2, 1, -2]) == False
assert monotonic([-1, 2, 1, -1]) == False
assert monotonic([-1, 2, 1, 0]) == False
assert monotonic([-1, 2, 1, 1]) == False
assert monotonic([-1, 2, 1, 2]) == False
assert monotonic([-1, 2, 2, -2]) == False
assert monotonic([-1, 2, 2, -1]) == False
assert monotonic([-1, 2, 2, 0]) == False
assert monotonic([-1, 2, 2, 1]) == False
assert monotonic([-1, 2, 2, 2]) == True
assert monotonic([0, -2, -2, -2]) == True
assert monotonic([0, -2, -2, -1]) == False
assert monotonic([0, -2, -2, 0]) == False
assert monotonic([0, -2, -2, 1]) == False
assert monotonic([0, -2, -2, 2]) == False
assert monotonic([0, -2, -1, -2]) == False
assert monotonic([0, -2, -1, -1]) == False
assert monotonic([0, -2, -1, 0]) == False
assert monotonic([0, -2, -1, 1]) == False
assert monotonic([0, -2, -1, 2]) == False
assert monotonic([0, -2, 0, -2]) == False
assert monotonic([0, -2, 0, -1]) == False
assert monotonic([0, -2, 0, 0]) == False
assert monotonic([0, -2, 0, 1]) == False
assert monotonic([0, -2, 0, 2]) == False
assert monotonic([0, -2, 1, -2]) == False
assert monotonic([0, -2, 1, -1]) == False
assert monotonic([0, -2, 1, 0]) == False
assert monotonic([0, -2, 1, 1]) == False
assert monotonic([0, -2, 1, 2]) == False
assert monotonic([0, -2, 2, -2]) == False
assert monotonic([0, -2, 2, -1]) == False
assert monotonic([0, -2, 2, 0]) == False
assert monotonic([0, -2, 2, 1]) == False
assert monotonic([0, -2, 2, 2]) == False
assert monotonic([0, -1, -2, -2]) == True
assert monotonic([0, -1, -2, -1]) == False
assert monotonic([0, -1, -2, 0]) == False
assert monotonic([0, -1, -2, 1]) == False
assert monotonic([0, -1, -2, 2]) == False
assert monotonic([0, -1, -1, -2]) == True
assert monotonic([0, -1, -1, -1]) == True
assert monotonic([0, -1, -1, 0]) == False
assert monotonic([0, -1, -1, 1]) == False
assert monotonic([0, -1, -1, 2]) == False
assert monotonic([0, -1, 0, -2]) == False
assert monotonic([0, -1, 0, -1]) == False
assert monotonic([0, -1, 0, 0]) == False
assert monotonic([0, -1, 0, 1]) == False
assert monotonic([0, -1, 0, 2]) == False
assert monotonic([0, -1, 1, -2]) == False
assert monotonic([0, -1, 1, -1]) == False
assert monotonic([0, -1, 1, 0]) == False
assert monotonic([0, -1, 1, 1]) == False
assert monotonic([0, -1, 1, 2]) == False
assert monotonic([0, -1, 2, -2]) == False
assert monotonic([0, -1, 2, -1]) == False
assert monotonic([0, -1, 2, 0]) == False
assert monotonic([0, -1, 2, 1]) == False
assert monotonic([0, -1, 2, 2]) == False
assert monotonic([0, 0, -2, -2]) == True
assert monotonic([0, 0, -2, -1]) == False
assert monotonic([0, 0, -2, 0]) == False
assert monotonic([0, 0, -2, 1]) == False
assert monotonic([0, 0, -2, 2]) == False
assert monotonic([0, 0, -1, -2]) == True
assert monotonic([0, 0, -1, -1]) == True
assert monotonic([0, 0, -1, 0]) == False
assert monotonic([0, 0, -1, 1]) == False
assert monotonic([0, 0, -1, 2]) == False
assert monotonic([0, 0, 0, -2]) == True
assert monotonic([0, 0, 0, -1]) == True
assert monotonic([0, 0, 0, 0]) == True
assert monotonic([0, 0, 0, 1]) == True
assert monotonic([0, 0, 0, 2]) == True
assert monotonic([0, 0, 1, -2]) == False
assert monotonic([0, 0, 1, -1]) == False
assert monotonic([0, 0, 1, 0]) == False
assert monotonic([0, 0, 1, 1]) == True
assert monotonic([0, 0, 1, 2]) == True
assert monotonic([0, 0, 2, -2]) == False
assert monotonic([0, 0, 2, -1]) == False
assert monotonic([0, 0, 2, 0]) == False
assert monotonic([0, 0, 2, 1]) == False
assert monotonic([0, 0, 2, 2]) == True
assert monotonic([0, 1, -2, -2]) == False
assert monotonic([0, 1, -2, -1]) == False
assert monotonic([0, 1, -2, 0]) == False
assert monotonic([0, 1, -2, 1]) == False
assert monotonic([0, 1, -2, 2]) == False
assert monotonic([0, 1, -1, -2]) == False
assert monotonic([0, 1, -1, -1]) == False
assert monotonic([0, 1, -1, 0]) == False
assert monotonic([0, 1, -1, 1]) == False
assert monotonic([0, 1, -1, 2]) == False
assert monotonic([0, 1, 0, -2]) == False
assert monotonic([0, 1, 0, -1]) == False
assert monotonic([0, 1, 0, 0]) == False
assert monotonic([0, 1, 0, 1]) == False
assert monotonic([0, 1, 0, 2]) == False
assert monotonic([0, 1, 1, -2]) == False
assert monotonic([0, 1, 1, -1]) == False
assert monotonic([0, 1, 1, 0]) == False
assert monotonic([0, 1, 1, 1]) == True
assert monotonic([0, 1, 1, 2]) == True
assert monotonic([0, 1, 2, -2]) == False
assert monotonic([0, 1, 2, -1]) == False
assert monotonic([0, 1, 2, 0]) == False
assert monotonic([0, 1, 2, 1]) == False
assert monotonic([0, 1, 2, 2]) == True
assert monotonic([0, 2, -2, -2]) == False
assert monotonic([0, 2, -2, -1]) == False
assert monotonic([0, 2, -2, 0]) == False
assert monotonic([0, 2, -2, 1]) == False
assert monotonic([0, 2, -2, 2]) == False
assert monotonic([0, 2, -1, -2]) == False
assert monotonic([0, 2, -1, -1]) == False
assert monotonic([0, 2, -1, 0]) == False
assert monotonic([0, 2, -1, 1]) == False
assert monotonic([0, 2, -1, 2]) == False
assert monotonic([0, 2, 0, -2]) == False
assert monotonic([0, 2, 0, -1]) == False
assert monotonic([0, 2, 0, 0]) == False
assert monotonic([0, 2, 0, 1]) == False
assert monotonic([0, 2, 0, 2]) == False
assert monotonic([0, 2, 1, -2]) == False
assert monotonic([0, 2, 1, -1]) == False
assert monotonic([0, 2, 1, 0]) == False
assert monotonic([0, 2, 1, 1]) == False
assert monotonic([0, 2, 1, 2]) == False
assert monotonic([0, 2, 2, -2]) == False
assert monotonic([0, 2, 2, -1]) == False
assert monotonic([0, 2, 2, 0]) == False
assert monotonic([0, 2, 2, 1]) == False
assert monotonic([0, 2, 2, 2]) == True
assert monotonic([1, -2, -2, -2]) == True
assert monotonic([1, -2, -2, -1]) == False
assert monotonic([1, -2, -2, 0]) == False
assert monotonic([1, -2, -2, 1]) == False
assert monotonic([1, -2, -2, 2]) == False
assert monotonic([1, -2, -1, -2]) == False
assert monotonic([1, -2, -1, -1]) == False
assert monotonic([1, -2, -1, 0]) == False
assert monotonic([1, -2, -1, 1]) == False
assert monotonic([1, -2, -1, 2]) == False
assert monotonic([1, -2, 0, -2]) == False
assert monotonic([1, -2, 0, -1]) == False
assert monotonic([1, -2, 0, 0]) == False
assert monotonic([1, -2, 0, 1]) == False
assert monotonic([1, -2, 0, 2]) == False
assert monotonic([1, -2, 1, -2]) == False
assert monotonic([1, -2, 1, -1]) == False
assert monotonic([1, -2, 1, 0]) == False
assert monotonic([1, -2, 1, 1]) == False
assert monotonic([1, -2, 1, 2]) == False
assert monotonic([1, -2, 2, -2]) == False
assert monotonic([1, -2, 2, -1]) == False
assert monotonic([1, -2, 2, 0]) == False
assert monotonic([1, -2, 2, 1]) == False
assert monotonic([1, -2, 2, 2]) == False
assert monotonic([1, -1, -2, -2]) == True
assert monotonic([1, -1, -2, -1]) == False
assert monotonic([1, -1, -2, 0]) == False
assert monotonic([1, -1, -2, 1]) == False
assert monotonic([1, -1, -2, 2]) == False
assert monotonic([1, -1, -1, -2]) == True
assert monotonic([1, -1, -1, -1]) == True
assert monotonic([1, -1, -1, 0]) == False
assert monotonic([1, -1, -1, 1]) == False
assert monotonic([1, -1, -1, 2]) == False
assert monotonic([1, -1, 0, -2]) == False
assert monotonic([1, -1, 0, -1]) == False
assert monotonic([1, -1, 0, 0]) == False
assert monotonic([1, -1, 0, 1]) == False
assert monotonic([1, -1, 0, 2]) == False
assert monotonic([1, -1, 1, -2]) == False
assert monotonic([1, -1, 1, -1]) == False
assert monotonic([1, -1, 1, 0]) == False
assert monotonic([1, -1, 1, 1]) == False
assert monotonic([1, -1, 1, 2]) == False
assert monotonic([1, -1, 2, -2]) == False
assert monotonic([1, -1, 2, -1]) == False
assert monotonic([1, -1, 2, 0]) == False
assert monotonic([1, -1, 2, 1]) == False
assert monotonic([1, -1, 2, 2]) == False
assert monotonic([1, 0, -2, -2]) == True
assert monotonic([1, 0, -2, -1]) == False
assert monotonic([1, 0, -2, 0]) == False
assert monotonic([1, 0, -2, 1]) == False
assert monotonic([1, 0, -2, 2]) == False
assert monotonic([1, 0, -1, -2]) == True
assert monotonic([1, 0, -1, -1]) == True
assert monotonic([1, 0, -1, 0]) == False
assert monotonic([1, 0, -1, 1]) == False
assert monotonic([1, 0, -1, 2]) == False
assert monotonic([1, 0, 0, -2]) == True
assert monotonic([1, 0, 0, -1]) == True
assert monotonic([1, 0, 0, 0]) == True
assert monotonic([1, 0, 0, 1]) == False
assert monotonic([1, 0, 0, 2]) == False
assert monotonic([1, 0, 1, -2]) == False
assert monotonic([1, 0, 1, -1]) == False
assert monotonic([1, 0, 1, 0]) == False
assert monotonic([1, 0, 1, 1]) == False
assert monotonic([1, 0, 1, 2]) == False
assert monotonic([1, 0, 2, -2]) == False
assert monotonic([1, 0, 2, -1]) == False
assert monotonic([1, 0, 2, 0]) == False
assert monotonic([1, 0, 2, 1]) == False
assert monotonic([1, 0, 2, 2]) == False
assert monotonic([1, 1, -2, -2]) == True
assert monotonic([1, 1, -2, -1]) == False
assert monotonic([1, 1, -2, 0]) == False
assert monotonic([1, 1, -2, 1]) == False
assert monotonic([1, 1, -2, 2]) == False
assert monotonic([1, 1, -1, -2]) == True
assert monotonic([1, 1, -1, -1]) == True
assert monotonic([1, 1, -1, 0]) == False
assert monotonic([1, 1, -1, 1]) == False
assert monotonic([1, 1, -1, 2]) == False
assert monotonic([1, 1, 0, -2]) == True
assert monotonic([1, 1, 0, -1]) == True
assert monotonic([1, 1, 0, 0]) == True
assert monotonic([1, 1, 0, 1]) == False
assert monotonic([1, 1, 0, 2]) == False
assert monotonic([1, 1, 1, -2]) == True
assert monotonic([1, 1, 1, -1]) == True
assert monotonic([1, 1, 1, 0]) == True
assert monotonic([1, 1, 1, 1]) == True
assert monotonic([1, 1, 1, 2]) == True
assert monotonic([1, 1, 2, -2]) == False
assert monotonic([1, 1, 2, -1]) == False
assert monotonic([1, 1, 2, 0]) == False
assert monotonic([1, 1, 2, 1]) == False
assert monotonic([1, 1, 2, 2]) == True
assert monotonic([1, 2, -2, -2]) == False
assert monotonic([1, 2, -2, -1]) == False
assert monotonic([1, 2, -2, 0]) == False
assert monotonic([1, 2, -2, 1]) == False
assert monotonic([1, 2, -2, 2]) == False
assert monotonic([1, 2, -1, -2]) == False
assert monotonic([1, 2, -1, -1]) == False
assert monotonic([1, 2, -1, 0]) == False
assert monotonic([1, 2, -1, 1]) == False
assert monotonic([1, 2, -1, 2]) == False
assert monotonic([1, 2, 0, -2]) == False
assert monotonic([1, 2, 0, -1]) == False
assert monotonic([1, 2, 0, 0]) == False
assert monotonic([1, 2, 0, 1]) == False
assert monotonic([1, 2, 0, 2]) == False
assert monotonic([1, 2, 1, -2]) == False
assert monotonic([1, 2, 1, -1]) == False
assert monotonic([1, 2, 1, 0]) == False
assert monotonic([1, 2, 1, 1]) == False
assert monotonic([1, 2, 1, 2]) == False
assert monotonic([1, 2, 2, -2]) == False
assert monotonic([1, 2, 2, -1]) == False
assert monotonic([1, 2, 2, 0]) == False
assert monotonic([1, 2, 2, 1]) == False
assert monotonic([1, 2, 2, 2]) == True
assert monotonic([2, -2, -2, -2]) == True
assert monotonic([2, -2, -2, -1]) == False
assert monotonic([2, -2, -2, 0]) == False
assert monotonic([2, -2, -2, 1]) == False
assert monotonic([2, -2, -2, 2]) == False
assert monotonic([2, -2, -1, -2]) == False
assert monotonic([2, -2, -1, -1]) == False
assert monotonic([2, -2, -1, 0]) == False
assert monotonic([2, -2, -1, 1]) == False
assert monotonic([2, -2, -1, 2]) == False
assert monotonic([2, -2, 0, -2]) == False
assert monotonic([2, -2, 0, -1]) == False
assert monotonic([2, -2, 0, 0]) == False
assert monotonic([2, -2, 0, 1]) == False
assert monotonic([2, -2, 0, 2]) == False
assert monotonic([2, -2, 1, -2]) == False
assert monotonic([2, -2, 1, -1]) == False
assert monotonic([2, -2, 1, 0]) == False
assert monotonic([2, -2, 1, 1]) == False
assert monotonic([2, -2, 1, 2]) == False
assert monotonic([2, -2, 2, -2]) == False
assert monotonic([2, -2, 2, -1]) == False
assert monotonic([2, -2, 2, 0]) == False
assert monotonic([2, -2, 2, 1]) == False
assert monotonic([2, -2, 2, 2]) == False
assert monotonic([2, -1, -2, -2]) == True
assert monotonic([2, -1, -2, -1]) == False
assert monotonic([2, -1, -2, 0]) == False
assert monotonic([2, -1, -2, 1]) == False
assert monotonic([2, -1, -2, 2]) == False
assert monotonic([2, -1, -1, -2]) == True
assert monotonic([2, -1, -1, -1]) == True
assert monotonic([2, -1, -1, 0]) == False
assert monotonic([2, -1, -1, 1]) == False
assert monotonic([2, -1, -1, 2]) == False
assert monotonic([2, -1, 0, -2]) == False
assert monotonic([2, -1, 0, -1]) == False
assert monotonic([2, -1, 0, 0]) == False
assert monotonic([2, -1, 0, 1]) == False
assert monotonic([2, -1, 0, 2]) == False
assert monotonic([2, -1, 1, -2]) == False
assert monotonic([2, -1, 1, -1]) == False
assert monotonic([2, -1, 1, 0]) == False
assert monotonic([2, -1, 1, 1]) == False
assert monotonic([2, -1, 1, 2]) == False
assert monotonic([2, -1, 2, -2]) == False
assert monotonic([2, -1, 2, -1]) == False
assert monotonic([2, -1, 2, 0]) == False
assert monotonic([2, -1, 2, 1]) == False
assert monotonic([2, -1, 2, 2]) == False
assert monotonic([2, 0, -2, -2]) == True
assert monotonic([2, 0, -2, -1]) == False
assert monotonic([2, 0, -2, 0]) == False
assert monotonic([2, 0, -2, 1]) == False
assert monotonic([2, 0, -2, 2]) == False
assert monotonic([2, 0, -1, -2]) == True
assert monotonic([2, 0, -1, -1]) == True
assert monotonic([2, 0, -1, 0]) == False
assert monotonic([2, 0, -1, 1]) == False
assert monotonic([2, 0, -1, 2]) == False
assert monotonic([2, 0, 0, -2]) == True
assert monotonic([2, 0, 0, -1]) == True
assert monotonic([2, 0, 0, 0]) == True
assert monotonic([2, 0, 0, 1]) == False
assert monotonic([2, 0, 0, 2]) == False
assert monotonic([2, 0, 1, -2]) == False
assert monotonic([2, 0, 1, -1]) == False
assert monotonic([2, 0, 1, 0]) == False
assert monotonic([2, 0, 1, 1]) == False
assert monotonic([2, 0, 1, 2]) == False
assert monotonic([2, 0, 2, -2]) == False
assert monotonic([2, 0, 2, -1]) == False
assert monotonic([2, 0, 2, 0]) == False
assert monotonic([2, 0, 2, 1]) == False
assert monotonic([2, 0, 2, 2]) == False
assert monotonic([2, 1, -2, -2]) == True
assert monotonic([2, 1, -2, -1]) == False
assert monotonic([2, 1, -2, 0]) == False
assert monotonic([2, 1, -2, 1]) == False
assert monotonic([2, 1, -2, 2]) == False
assert monotonic([2, 1, -1, -2]) == True
assert monotonic([2, 1, -1, -1]) == True
assert monotonic([2, 1, -1, 0]) == False
assert monotonic([2, 1, -1, 1]) == False
assert monotonic([2, 1, -1, 2]) == False
assert monotonic([2, 1, 0, -2]) == True
assert monotonic([2, 1, 0, -1]) == True
assert monotonic([2, 1, 0, 0]) == True
assert monotonic([2, 1, 0, 1]) == False
assert monotonic([2, 1, 0, 2]) == False
assert monotonic([2, 1, 1, -2]) == True
assert monotonic([2, 1, 1, -1]) == True
assert monotonic([2, 1, 1, 0]) == True
assert monotonic([2, 1, 1, 1]) == True
assert monotonic([2, 1, 1, 2]) == False
assert monotonic([2, 1, 2, -2]) == False
assert monotonic([2, 1, 2, -1]) == False
assert monotonic([2, 1, 2, 0]) == False
assert monotonic([2, 1, 2, 1]) == False
assert monotonic([2, 1, 2, 2]) == False
assert monotonic([2, 2, -2, -2]) == True
assert monotonic([2, 2, -2, -1]) == False
assert monotonic([2, 2, -2, 0]) == False
assert monotonic([2, 2, -2, 1]) == False
assert monotonic([2, 2, -2, 2]) == False
assert monotonic([2, 2, -1, -2]) == True
assert monotonic([2, 2, -1, -1]) == True
assert monotonic([2, 2, -1, 0]) == False
assert monotonic([2, 2, -1, 1]) == False
assert monotonic([2, 2, -1, 2]) == False
assert monotonic([2, 2, 0, -2]) == True
assert monotonic([2, 2, 0, -1]) == True
assert monotonic([2, 2, 0, 0]) == True
assert monotonic([2, 2, 0, 1]) == False
assert monotonic([2, 2, 0, 2]) == False
assert monotonic([2, 2, 1, -2]) == True
assert monotonic([2, 2, 1, -1]) == True
assert monotonic([2, 2, 1, 0]) == True
assert monotonic([2, 2, 1, 1]) == True
assert monotonic([2, 2, 1, 2]) == False
assert monotonic([2, 2, 2, -2]) == True
assert monotonic([2, 2, 2, -1]) == True
assert monotonic([2, 2, 2, 0]) == True
assert monotonic([2, 2, 2, 1]) == True
assert monotonic([2, 2, 2, 2]) == True

# generated_cases=781
