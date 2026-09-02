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
assert fizz_buzz(1) == 0
assert fizz_buzz(50) == 0
assert fizz_buzz(77) == 0
assert fizz_buzz(78) == 2
assert fizz_buzz(79) == 3
assert fizz_buzz(117) == 3
assert fizz_buzz(118) == 4
assert fizz_buzz(143) == 4
assert fizz_buzz(144) == 4
assert fizz_buzz(176) == 4
assert fizz_buzz(177) == 5
assert fizz_buzz(178) == 5
assert fizz_buzz(187) == 5
assert fizz_buzz(188) == 6
assert fizz_buzz(777) == 37
assert fizz_buzz(1000) == 47
