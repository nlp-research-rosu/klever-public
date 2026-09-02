def rounded_avg(n, m):
    if n > m:
        return -1

    total = n + m
    average = total // 2
    if total % 2 == 1:
        if average % 2 == 1:
            average = average + 1

    return bin(average)


assert rounded_avg(1, 5) == "0b11"
assert rounded_avg(7, 5) == -1
assert rounded_avg(10, 20) == "0b1111"
assert rounded_avg(20, 33) == "0b11010"

# Integral, half-even-down, and half-even-up representatives.
assert rounded_avg(1, 1) == "0b1"
assert rounded_avg(1, 2) == "0b10"
assert rounded_avg(2, 3) == "0b10"
assert rounded_avg(4, 5) == "0b100"
assert rounded_avg(99, 100) == "0b1100100"
