def sort_array(array):
    n = len(array)
    if n == 0:
        return []
    rev = (array[0] + array[-1]) % 2 == 0
    s = sorted(array)
    res = []
    i = 0
    for i in range(0, n):
        if rev:
            res = res + [s[n - 1 - i]]
        else:
            res = res + [s[i]]
    return res
