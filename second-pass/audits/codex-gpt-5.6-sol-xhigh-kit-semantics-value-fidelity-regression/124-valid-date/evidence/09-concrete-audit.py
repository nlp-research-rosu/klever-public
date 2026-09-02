def valid_date(date):
    if len(date) != 10:
        return False

    if date[2] != "-":
        return False
    if date[5] != "-":
        return False

    if date[0] < "0" or date[0] > "9":
        return False
    if date[1] < "0" or date[1] > "9":
        return False
    if date[3] < "0" or date[3] > "9":
        return False
    if date[4] < "0" or date[4] > "9":
        return False
    if date[6] < "0" or date[6] > "9":
        return False
    if date[7] < "0" or date[7] > "9":
        return False
    if date[8] < "0" or date[8] > "9":
        return False
    if date[9] < "0" or date[9] > "9":
        return False

    month_text = date[:2]
    day_text = date[3:5]

    month = int(month_text)
    day = int(day_text)

    if month < 1 or month > 12:
        return False
    if day < 1:
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
assert valid_date("01-01-0000") == True
assert valid_date("00-01-2000") == False
assert valid_date("13-01-2000") == False
assert valid_date("02-00-2000") == False
assert valid_date("02-29-2000") == True
assert valid_date("02-30-2000") == False
assert valid_date("04-30-2000") == True
assert valid_date("04-31-2000") == False
assert valid_date("01-31-2000") == True
assert valid_date("01-32-2000") == False
assert valid_date("03-11-20A0") == False
assert valid_date("03-11-20000") == False
