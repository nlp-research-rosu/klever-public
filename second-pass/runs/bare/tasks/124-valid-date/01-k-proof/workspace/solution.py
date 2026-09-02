def valid_date(date):
    if len(date) != 10:
        return False

    if date[2] != "-" or date[5] != "-":
        return False

    month_text = date[0:2]
    day_text = date[3:5]
    year_text = date[6:10]

    if not (month_text.isdigit() and day_text.isdigit() and year_text.isdigit()):
        return False

    month = int(month_text)
    day = int(day_text)

    if month < 1 or month > 12:
        return False

    if month == 2:
        return day >= 1 and day <= 29

    if month == 4 or month == 6 or month == 9 or month == 11:
        return day >= 1 and day <= 30

    return day >= 1 and day <= 31
