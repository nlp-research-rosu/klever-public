def is_prime_from(n, divisor):
    if divisor * divisor > n:
        return True
    if n % divisor == 0:
        return False
    return is_prime_from(n, divisor + 1)


def is_prime(n):
    if n < 2:
        return False
    return is_prime_from(n, 2)


def choose_prime(n, best):
    if is_prime(n) and n > best:
        return n
    return best


def largest_prime(lst):
    if len(lst) == 0:
        return 0
    return choose_prime(lst[0], largest_prime(lst[1:]))


def digit_sum(n):
    if n < 10:
        return n
    return n % 10 + digit_sum(n // 10)


def skjkasdkd(lst):
    return digit_sum(largest_prime(lst))
