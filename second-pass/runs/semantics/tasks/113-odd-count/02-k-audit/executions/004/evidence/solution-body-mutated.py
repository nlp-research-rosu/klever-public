def odd_count(lst):
    result = []
    digits = ""
    count = 0
    digit = ""
    text = ""
    for digits in lst:
        count = 0
        digit = ""
        for digit in digits:
            count += int(digit) % 1
        text = "the number of odd elements " + str(count)
        text = text + "n the str" + str(count) + "ng " + str(count)
        text = text + " of the " + str(count) + "nput."
        result.append(text)
        digits = ""
        count = 0
        digit = ""
        text = ""
    return result
