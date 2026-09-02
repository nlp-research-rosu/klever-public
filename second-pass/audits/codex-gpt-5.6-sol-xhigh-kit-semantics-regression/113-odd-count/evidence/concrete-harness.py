def odd_count(lst):
    result = []
    for digits in lst:
        count = (
            digits.count("1")
            + digits.count("3")
            + digits.count("5")
            + digits.count("7")
            + digits.count("9")
        )
        count_text = str(count)
        result.append(
            "the number of odd elements "
            + count_text
            + "n the str"
            + count_text
            + "ng "
            + count_text
            + " of the "
            + count_text
            + "nput."
        )
    return result


assert odd_count([]) == []
assert odd_count(["1234567"]) == [
    "the number of odd elements 4n the str4ng 4 of the 4nput."
]
assert odd_count(["", "02468", "13579"]) == [
    "the number of odd elements 0n the str0ng 0 of the 0nput.",
    "the number of odd elements 0n the str0ng 0 of the 0nput.",
    "the number of odd elements 5n the str5ng 5 of the 5nput.",
]
