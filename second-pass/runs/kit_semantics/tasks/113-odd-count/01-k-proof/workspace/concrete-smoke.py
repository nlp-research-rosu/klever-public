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


assert odd_count(["1234567"]) == [
    "the number of odd elements 4n the str4ng 4 of the 4nput."
]
assert odd_count(["3", "11111111"]) == [
    "the number of odd elements 1n the str1ng 1 of the 1nput.",
    "the number of odd elements 8n the str8ng 8 of the 8nput.",
]
assert odd_count(["", "135791357913"]) == [
    "the number of odd elements 0n the str0ng 0 of the 0nput.",
    "the number of odd elements 12n the str12ng 12 of the 12nput.",
]
