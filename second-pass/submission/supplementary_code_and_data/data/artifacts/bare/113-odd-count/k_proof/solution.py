def odd_count(lst):
    result = []
    for s in lst:
        count = 0
        for c in s:
            if c in "13579":
                count = count + 1
        result = result + ["the number of odd elements " + str(count) + "n the str" + str(count) + "ng " + str(count) + " of the " + str(count) + "nput."]
    return result
