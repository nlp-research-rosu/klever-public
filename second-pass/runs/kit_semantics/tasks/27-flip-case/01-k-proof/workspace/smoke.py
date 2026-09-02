def flip_case(string: str) -> str:
    return string.swapcase()


assert flip_case("Hello") == "hELLO"
assert flip_case("") == ""
assert flip_case("aZ 123!?") == "Az 123!?"
