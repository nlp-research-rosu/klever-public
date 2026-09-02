def valid_date(date):
    date = date.strip()
    parts = date.split('-')
    if len(parts) != 3:
        return False
    month, day, year = parts
    if not (month.isdigit() and day.isdigit() and year.isdigit()):
        return False
    month, day, year = int(month), int(day), int(year)
    if month < 1 or month > 12:
        return False
    if month in [1,3,5,7,8,10,12] and day < 1 or day > 31:
        return False
    if month in [4,6,9,11] and day < 1 or day > 30:
        return False
    if month == 2 and day < 1 or day > 29:
        return False
    return True
