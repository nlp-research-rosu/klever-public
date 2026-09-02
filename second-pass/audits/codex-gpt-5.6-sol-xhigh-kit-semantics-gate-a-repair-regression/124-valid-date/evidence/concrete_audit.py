def valid_date(date):
    if len(date) != 10:
        return False
    if date[2] != "-" or date[5] != "-":
        return False

    c0 = ord(date[0])
    c1 = ord(date[1])
    c3 = ord(date[3])
    c4 = ord(date[4])
    c6 = ord(date[6])
    c7 = ord(date[7])
    c8 = ord(date[8])
    c9 = ord(date[9])

    if (
        c0 < 48 or c0 > 57 or c1 < 48 or c1 > 57
        or c3 < 48 or c3 > 57 or c4 < 48 or c4 > 57
        or c6 < 48 or c6 > 57 or c7 < 48 or c7 > 57
        or c8 < 48 or c8 > 57 or c9 < 48 or c9 > 57
    ):
        return False

    month = (c0 - 48) * 10 + c1 - 48
    day = (c3 - 48) * 10 + c4 - 48

    if month < 1 or month > 12 or day < 1:
        return False
    if month == 2:
        return day <= 29
    if month == 4 or month == 6 or month == 9 or month == 11:
        return day <= 30
    return day <= 31


# Prompt examples.
assert valid_date("03-11-2000")
assert not valid_date("15-01-2012")
assert not valid_date("04-0-2040")
assert valid_date("06-04-2020")
assert not valid_date("06/04/2020")

# Every material return branch and boundary.
assert not valid_date("")
assert not valid_date("03/11-2000")
assert not valid_date("03-11/2000")
assert not valid_date("a3-11-2000")
assert not valid_date("03-a1-2000")
assert not valid_date("03-11-200a")
assert not valid_date("00-01-2000")
assert not valid_date("13-01-2000")
assert not valid_date("01-00-2000")
assert valid_date("02-29-2000")
assert not valid_date("02-30-2000")
assert valid_date("04-30-2000")
assert not valid_date("04-31-2000")
assert valid_date("01-31-2000")
assert not valid_date("01-32-2000")

# Canonical.py rejects these last two valid boundaries due to its Boolean
# grouping, while the prompt contract and generated program accept them.
