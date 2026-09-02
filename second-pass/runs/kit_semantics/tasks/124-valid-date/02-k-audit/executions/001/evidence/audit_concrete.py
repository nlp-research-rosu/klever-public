def valid_date(date):
    if len(date) != 10:
        return False

    if date[2] != "-" or date[5] != "-":
        return False

    month_tens = ord(date[0]) - 48
    month_ones = ord(date[1]) - 48
    day_tens = ord(date[3]) - 48
    day_ones = ord(date[4]) - 48
    year_thousands = ord(date[6]) - 48
    year_hundreds = ord(date[7]) - 48
    year_tens = ord(date[8]) - 48
    year_ones = ord(date[9]) - 48

    if month_tens < 0 or month_tens > 9:
        return False
    if month_ones < 0 or month_ones > 9:
        return False
    if day_tens < 0 or day_tens > 9:
        return False
    if day_ones < 0 or day_ones > 9:
        return False
    if year_thousands < 0 or year_thousands > 9:
        return False
    if year_hundreds < 0 or year_hundreds > 9:
        return False
    if year_tens < 0 or year_tens > 9:
        return False
    if year_ones < 0 or year_ones > 9:
        return False

    month = month_tens * 10 + month_ones
    day = day_tens * 10 + day_ones

    if month == 2:
        return day >= 1 and day <= 29
    if month == 4 or month == 6 or month == 9 or month == 11:
        return day >= 1 and day <= 30
    if (month == 1 or month == 3 or month == 5 or month == 7
            or month == 8 or month == 10 or month == 12):
        return day >= 1 and day <= 31
    return False


assert valid_date("03-11-2000") == True
assert valid_date("01-31-0000") == True
assert valid_date("04-30-9999") == True
assert valid_date("02-29-2001") == True
assert valid_date("02-30-2000") == False
assert valid_date("04-31-2000") == False
assert valid_date("00-01-2000") == False
assert valid_date("13-01-2000") == False
assert valid_date("01-00-2000") == False
assert valid_date("01-32-2000") == False
assert valid_date("03/11/2000") == False
assert valid_date("03-11-200") == False
assert valid_date("03-11-20000") == False
assert valid_date("0a-11-2000") == False
assert valid_date("03-11-20c0") == False
