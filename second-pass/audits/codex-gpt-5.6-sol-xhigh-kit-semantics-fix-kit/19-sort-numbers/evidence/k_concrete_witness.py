def sort_numbers(numbers: str) -> str:
    order = (
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    )
    return " ".join(sorted(numbers.split(), key=order.index))


assert sort_numbers("three one five") == "one three five"
assert sort_numbers("") == ""
assert sort_numbers("nine eight seven six five four three two one zero") == (
    "zero one two three four five six seven eight nine"
)
assert sort_numbers("nine zero nine zero five five") == "zero zero five five nine nine"
