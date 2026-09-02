def rounded_avg(n, m):
    if n > m:
        return -1
    value = (n + m) // 2 + (n + m) % 2 * ((n + m) // 2 % 2)
    digits = ""
    while value > 1:
        digits = chr(48 + value % 2) + digits
        value = value // 2
    digits = "1" + digits
    return "0b" + digits
