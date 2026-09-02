def flip_case(string):
    return string.swapcase()


# HumanEval/27 test cases (the dataset `check`); returns a string.
assert flip_case("") == ""
assert flip_case("Hello!") == "hELLO!"
assert flip_case("These violent delights have violent ends") == "tHESE VIOLENT DELIGHTS HAVE VIOLENT ENDS"
