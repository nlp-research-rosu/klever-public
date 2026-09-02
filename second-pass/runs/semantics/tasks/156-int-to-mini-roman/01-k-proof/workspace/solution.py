def _roman_thousands(digit):
    return ("", "m")[digit]


def _roman_hundreds(digit):
    return ("", "c", "cc", "ccc", "cd", "d", "dc", "dcc", "dccc", "cm")[digit]


def _roman_tens(digit):
    return ("", "x", "xx", "xxx", "xl", "l", "lx", "lxx", "lxxx", "xc")[digit]


def _roman_ones(digit):
    return ("", "i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix")[digit]


def int_to_mini_roman(number):
    return (
        _roman_thousands(number // 1000)
        + _roman_hundreds((number % 1000) // 100)
        + _roman_tens((number % 100) // 10)
        + _roman_ones(number % 10)
    )
