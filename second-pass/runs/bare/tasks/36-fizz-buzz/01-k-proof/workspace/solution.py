def fizz_buzz(n: int):
    count = 0
    i = 0
    while i < n:
        if i % 11 == 0 or i % 13 == 0:
            x = i
            while x > 0:
                if x % 10 == 7:
                    count = count + 1
                x = x // 10
        i = i + 1
    return count
