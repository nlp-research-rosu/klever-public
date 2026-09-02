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
