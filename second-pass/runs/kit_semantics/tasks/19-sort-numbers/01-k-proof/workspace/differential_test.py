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


def counting_oracle(numbers: str) -> str:
    result = []
    for word in (
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
    ):
        for item in numbers.split():
            if item == word:
                result.append(item)
    return " ".join(result)


cases = [
    "",
    "zero",
    "nine",
    "three one five",
    "nine zero nine",
    "one one one",
    "nine eight seven six five four three two one zero",
    "zero one two three four five six seven eight nine",
    "five zero four one three two",
    "eight two eight two zero",
    "  three   one five  ",
    "zero nine one eight two seven three six four five",
    "six six five five four four three three two two one one zero zero",
    "nine zero eight one seven two six three five four",
    "two seven one eight zero nine three six four five two seven",
]

for case in cases:
    assert sort_numbers(case) == counting_oracle(case)
