def change_base(x: int, base: int):
    """Change numerical base of input number x to base.
    return string representation after the conversion.
    base numbers are less than 10.
    >>> change_base(8, 3)
    '22'
    >>> change_base(8, 2)
    '1000'
    >>> change_base(7, 2)
    '111'
    """
    if x == 0:
        return ""
    return change_base(x // base, base) + chr(48 + x % base)


assert change_base(8, 3) == "22"
assert change_base(8, 2) == "1000"
assert change_base(7, 2) == "111"
assert change_base(0, 2) == ""
assert change_base(31, 5) == "111"
assert change_base(999, 9) == "1330"
