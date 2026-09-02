def sort_numbers(numbers: str) -> str:
    return " ".join(
        sorted(
            numbers.split(),
            key=lambda word: {
                "zero": 0,
                "one": 1,
                "two": 2,
                "three": 3,
                "four": 4,
                "five": 5,
                "six": 6,
                "seven": 7,
                "eight": 8,
                "nine": 9,
            }[word],
        )
    )


assert sort_numbers("") == ""
assert sort_numbers("three one five") == "one three five"
assert sort_numbers("nine zero five one one") == "zero one one five nine"
assert sort_numbers(
    "nine eight seven six five four three two one zero"
) == "zero one two three four five six seven eight nine"
assert sort_numbers("  three   one five  ") == "one three five"
