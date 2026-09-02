def unique_digits(x):
    result = []
    n = 1
    odd = True
    y = 0
    for n in x:
        odd = True
        y = n
        while y > 0:
            if y % 2 == 0:
                odd = False
            y = y // 10
        if odd:
            result.append(n)
    result.sort()
    return result


assert unique_digits([15, 33, 1422, 1]) == [1, 15, 33]
assert unique_digits([152, 323, 1422, 10]) == []
assert unique_digits([]) == []
assert unique_digits([1]) == [1]
assert unique_digits([2]) == []
assert unique_digits([99, 15, 15, 1]) == [1, 15, 15, 99]
assert unique_digits([101, 111, 13579, 20]) == [111, 13579]
