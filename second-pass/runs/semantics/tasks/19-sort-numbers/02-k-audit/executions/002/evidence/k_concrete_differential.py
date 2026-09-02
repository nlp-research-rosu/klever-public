def number_value(word: str) -> int:
    if word == "zero":
        return 0
    if word == "one":
        return 1
    if word == "two":
        return 2
    if word == "three":
        return 3
    if word == "four":
        return 4
    if word == "five":
        return 5
    if word == "six":
        return 6
    if word == "seven":
        return 7
    if word == "eight":
        return 8
    return 9


def sort_numbers(numbers: str) -> str:
    return " ".join(sorted(numbers.split(), key=number_value))


assert sort_numbers("") == ""
assert sort_numbers("three one five") == "one three five"
assert sort_numbers("zero") == "zero"
assert sort_numbers("one") == "one"
assert sort_numbers("two") == "two"
assert sort_numbers("three") == "three"
assert sort_numbers("four") == "four"
assert sort_numbers("five") == "five"
assert sort_numbers("six") == "six"
assert sort_numbers("seven") == "seven"
assert sort_numbers("eight") == "eight"
assert sort_numbers("nine") == "nine"
assert sort_numbers("nine zero") == "zero nine"
assert sort_numbers("eight one seven two") == "one two seven eight"
assert sort_numbers("nine zero nine two one") == "zero one two nine nine"
assert sort_numbers("nine eight seven six five four three two one zero") == "zero one two three four five six seven eight nine"
assert sort_numbers("two two zero nine zero two") == "zero zero two two two nine"
assert sort_numbers("  three one five") == "one three five"
assert sort_numbers("three   one  five") == "one three five"
assert sort_numbers("three one five  ") == "one three five"
