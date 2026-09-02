def _number_key(number: str) -> int:
    return (
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
    ).index(number)


def sort_numbers(numbers: str) -> str:
    return " ".join(sorted(numbers.split(), key=_number_key))


assert sort_numbers("") == ""
assert sort_numbers("three one five") == "one three five"
assert sort_numbers("nine zero nine") == "zero nine nine"
assert (
    sort_numbers("nine eight seven six five four three two one zero")
    == "zero one two three four five six seven eight nine"
)
