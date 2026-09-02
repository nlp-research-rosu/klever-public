def int_to_mini_roman(number):
    thousands = ("", "m")
    hundreds = ("", "c", "cc", "ccc", "cd", "d", "dc", "dcc", "dccc", "cm")
    tens = ("", "x", "xx", "xxx", "xl", "l", "lx", "lxx", "lxxx", "xc")
    ones = ("", "i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix")
    return (
        thousands[number // 1000]
        + hundreds[(number % 1000) // 100]
        + tens[(number % 100) // 10]
        + ones[number % 10]
    )
