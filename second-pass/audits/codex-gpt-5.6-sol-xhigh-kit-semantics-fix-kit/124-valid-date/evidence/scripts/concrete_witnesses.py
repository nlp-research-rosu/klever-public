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

    if (month_tens < 0 or month_tens > 9 or
            month_ones < 0 or month_ones > 9 or
            day_tens < 0 or day_tens > 9 or
            day_ones < 0 or day_ones > 9 or
            year_thousands < 0 or year_thousands > 9 or
            year_hundreds < 0 or year_hundreds > 9 or
            year_tens < 0 or year_tens > 9 or
            year_ones < 0 or year_ones > 9):
        return False

    month = month_tens * 10 + month_ones
    day = day_tens * 10 + day_ones

    if month < 1 or month > 12 or day < 1:
        return False
    if month == 2:
        return day <= 29
    if month == 4 or month == 6 or month == 9 or month == 11:
        return day <= 30
    return day <= 31


assert valid_date("") == False
assert valid_date("03-11-2000") == True
assert valid_date("03-31-2000") == True
assert valid_date("02-30-2000") == False
assert valid_date("04-31-2000") == False
