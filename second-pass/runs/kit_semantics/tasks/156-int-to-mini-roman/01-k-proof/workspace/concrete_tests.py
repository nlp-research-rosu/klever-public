def int_to_mini_roman(number):
    hundreds = (
        "", "c", "cc", "ccc", "cd", "d", "dc", "dcc", "dccc", "cm"
    )[(number % 1000) // 100]
    tens = (
        "", "x", "xx", "xxx", "xl", "l", "lx", "lxx", "lxxx", "xc"
    )[(number % 100) // 10]
    ones = (
        "", "i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix"
    )[number % 10]
    if number == 1000:
        return "m"
    return hundreds + tens + ones


sample_19 = int_to_mini_roman(19)
sample_152 = int_to_mini_roman(152)
sample_426 = int_to_mini_roman(426)
boundary_1 = int_to_mini_roman(1)
boundary_1000 = int_to_mini_roman(1000)
