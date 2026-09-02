def odd_count(lst):
    res = []
    for arr in lst:
        n = 0
        for d in arr:
            if int(d) % 2 == 1:
                n = n + 1
        res.append("the number of odd elements " + str(n) + "n the str" + str(n) + "ng " + str(n) + " of the " + str(n) + "nput.")
    return res
