def valid_date(date):
    if len(date) != 10:
        return False

    if date[2] != "-" or date[5] != "-":
        return False

    if (
        ord(date[0]) < 48
        or ord(date[0]) > 57
        or ord(date[1]) < 48
        or ord(date[1]) > 57
        or ord(date[3]) < 48
        or ord(date[3]) > 57
        or ord(date[4]) < 48
        or ord(date[4]) > 57
        or ord(date[6]) < 48
        or ord(date[6]) > 57
        or ord(date[7]) < 48
        or ord(date[7]) > 57
        or ord(date[8]) < 48
        or ord(date[8]) > 57
        or ord(date[9]) < 48
        or ord(date[9]) > 57
    ):
        return False

    month = int(date[0:2])
    day = int(date[3:5])

    if month < 1 or month > 12 or day < 1:
        return False

    if month == 2:
        return day <= 29

    if month == 4 or month == 6 or month == 9 or month == 11:
        return day <= 30

    return day <= 31


assert valid_date("03-11-2000") == True
assert valid_date("15-01-2012") == False
assert valid_date("04-0-2040") == False
assert valid_date("06-04-2020") == True
assert valid_date("06/04/2020") == False
assert valid_date("") == False
assert valid_date(" 03-11-2000 ") == False
assert valid_date("01-01-20a0") == False
assert valid_date("00-01-2000") == False
assert valid_date("13-01-2000") == False
assert valid_date("01-00-2000") == False
assert valid_date("01-31-2000") == True
assert valid_date("01-32-2000") == False
assert valid_date("02-29-2000") == True
assert valid_date("02-30-2000") == False
assert valid_date("04-30-2000") == True
assert valid_date("04-31-2000") == False
assert valid_date("12-31-9999") == True
