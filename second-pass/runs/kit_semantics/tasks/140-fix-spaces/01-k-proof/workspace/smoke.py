def fix_spaces(text):
    result = ""
    spaces = ""
    char = ""
    for char in text:
        if char == " ":
            if spaces == "__":
                spaces = "-"
            elif spaces != "-":
                spaces += "_"
        else:
            result += spaces + char
            spaces = ""
    return result + spaces


assert fix_spaces("") == ""
assert fix_spaces("Example") == "Example"
assert fix_spaces("Example 1") == "Example_1"
assert fix_spaces(" Example 2") == "_Example_2"
assert fix_spaces(" Example   3") == "_Example-3"
assert fix_spaces("a  b    c ") == "a__b-c_"
