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


assert rounded_avg(1, 5) == "0b11"
assert rounded_avg(7, 5) == -1
assert rounded_avg(10, 20) == "0b1111"
assert rounded_avg(20, 33) == "0b11010"
assert rounded_avg(1, 1) == "0b1"
assert rounded_avg(2, 2) == "0b10"
