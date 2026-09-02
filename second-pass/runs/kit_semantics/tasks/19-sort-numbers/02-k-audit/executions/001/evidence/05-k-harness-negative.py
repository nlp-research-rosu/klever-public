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


assert sort_numbers("three one five") == "three one five"
