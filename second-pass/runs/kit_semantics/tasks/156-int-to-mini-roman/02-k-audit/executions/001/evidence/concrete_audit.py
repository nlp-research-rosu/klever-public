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


result_1 = int_to_mini_roman(1)
result_4 = int_to_mini_roman(4)
result_9 = int_to_mini_roman(9)
result_40 = int_to_mini_roman(40)
result_90 = int_to_mini_roman(90)
result_400 = int_to_mini_roman(400)
result_900 = int_to_mini_roman(900)
result_1000 = int_to_mini_roman(1000)
