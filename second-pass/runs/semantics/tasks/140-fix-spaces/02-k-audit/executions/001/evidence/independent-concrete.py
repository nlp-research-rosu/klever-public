def fix_spaces(text):
    result = ""
    spaces = 0
    char = ""

    for char in text:
        if ord(char) - 32:
            if spaces > 2:
                result += "-"
            elif spaces == 1:
                result += "_"
            elif spaces == 2:
                result += "__"

            result += char
            spaces = 0
        else:
            spaces += 1

    if spaces > 2:
        result += "-"
    elif spaces == 1:
        result += "_"
    elif spaces == 2:
        result += "__"

    return result


# Reviewer-selected documented, empty, and branch-boundary cases.
assert fix_spaces("") == ""
assert fix_spaces("Example") == "Example"
assert fix_spaces("Example 1") == "Example_1"
assert fix_spaces(" Example 2") == "_Example_2"
assert fix_spaces(" Example   3") == "_Example-3"
assert fix_spaces(" ") == "_"
assert fix_spaces("  ") == "__"
assert fix_spaces("   ") == "-"
assert fix_spaces("    ") == "-"
assert fix_spaces("a ") == "a_"
assert fix_spaces("a  ") == "a__"
assert fix_spaces("a   ") == "a-"
assert fix_spaces(" a") == "_a"
assert fix_spaces("  a") == "__a"
assert fix_spaces("   a") == "-a"
assert fix_spaces("a b") == "a_b"
assert fix_spaces("a  b") == "a__b"
assert fix_spaces("a   b") == "a-b"
assert fix_spaces("  a   b  ") == "__a-b__"
