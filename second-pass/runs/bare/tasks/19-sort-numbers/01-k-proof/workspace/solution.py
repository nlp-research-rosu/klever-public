def sort_numbers(numbers: str) -> str:
    return (
        "zero " * numbers.count("zero")
        + "one " * numbers.count("one")
        + "two " * numbers.count("two")
        + "three " * numbers.count("three")
        + "four " * numbers.count("four")
        + "five " * numbers.count("five")
        + "six " * numbers.count("six")
        + "seven " * numbers.count("seven")
        + "eight " * numbers.count("eight")
        + "nine " * numbers.count("nine")
    ).strip()
