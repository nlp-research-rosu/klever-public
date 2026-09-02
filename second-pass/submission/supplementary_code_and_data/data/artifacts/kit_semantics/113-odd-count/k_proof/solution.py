def odd_count(lst):
    result = []
    s = ""
    count = 0
    count_string = ""
    for s in lst:
        count = (
            s.count("1")
            + s.count("3")
            + s.count("5")
            + s.count("7")
            + s.count("9")
        )
        count_string = str(count)
        result.append(
            "the number of odd elements "
            + count_string
            + "n the str"
            + count_string
            + "ng "
            + count_string
            + " of the "
            + count_string
            + "nput."
        )
    return result
