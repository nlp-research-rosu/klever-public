def valid_date(date):
    if len(date) != 10:
        return False

    if ord(date[2]) != 45 or ord(date[5]) != 45:
        return False

    m0 = ord(date[0])
    m1 = ord(date[1])
    d0 = ord(date[3])
    d1 = ord(date[4])
    y0 = ord(date[6])
    y1 = ord(date[7])
    y2 = ord(date[8])
    y3 = ord(date[9])

    if (
        m0 < 48 or m0 > 57
        or m1 < 48 or m1 > 57
        or d0 < 48 or d0 > 57
        or d1 < 48 or d1 > 57
        or y0 < 48 or y0 > 57
        or y1 < 48 or y1 > 57
        or y2 < 48 or y2 > 57
        or y3 < 48 or y3 > 57
    ):
        return False

    month = (m0 - 48) * 10 + m1 - 48
    day = (d0 - 48) * 10 + d1 - 48

    if month < 1 or month > 12:
        return False
    if day < 1:
        return False

    if month == 2:
        return day <= 29
    if month == 4 or month == 6 or month == 9 or month == 11:
        return day <= 30
    return day <= 31
