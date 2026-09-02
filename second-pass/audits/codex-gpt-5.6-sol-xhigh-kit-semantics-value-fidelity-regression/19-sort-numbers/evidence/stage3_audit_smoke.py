def _number_rank(number: str) -> int:
    if number == "zero":
        return 0
    if number == "one":
        return 1
    if number == "two":
        return 2
    if number == "three":
        return 3
    if number == "four":
        return 4
    if number == "five":
        return 5
    if number == "six":
        return 6
    if number == "seven":
        return 7
    if number == "eight":
        return 8
    return 9


def sort_numbers(numbers: str) -> str:
    return " ".join(sorted(numbers.split(), key=_number_rank))


assert sort_numbers("three one five") == "one three five"
assert sort_numbers("") == ""
assert sort_numbers("   ") == ""
assert sort_numbers("zero") == "zero"
assert sort_numbers("nine") == "nine"
assert sort_numbers("nine zero eight one") == "zero one eight nine"
assert sort_numbers("nine nine zero zero five") == "zero zero five nine nine"
assert sort_numbers("  eight   two zero  ") == "zero two eight"
assert sort_numbers("three\tone\nfive") == "one three five"
