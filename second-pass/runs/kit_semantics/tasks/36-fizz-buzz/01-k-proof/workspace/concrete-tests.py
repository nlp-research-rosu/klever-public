def fizz_buzz(n: int):
    count = 0
    i = n
    x = 0
    while i > 0:
        i = i - 1
        if i % 11 == 0 or i % 13 == 0:
            x = i
            while x > 0:
                count = count + (x % 10 == 7)
                x = x // 10
    return count


assert fizz_buzz(-5) == 0
assert fizz_buzz(0) == 0
assert fizz_buzz(50) == 0
assert fizz_buzz(78) == 2
assert fizz_buzz(79) == 3
assert fizz_buzz(177) == 5
assert fizz_buzz(777) == 37
