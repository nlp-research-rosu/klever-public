def odd_digits_product(n):
    if n <= 0:
        return 1
    quotient = (n - (n % 10)) // 10
    if n % 2 == 1:
        return (n % 10) * odd_digits_product(quotient)
    return odd_digits_product(quotient)


def odd_digit_seen(n):
    if n <= 0:
        return 0
    quotient = (n - (n % 10)) // 10
    if n % 2 == 1:
        return 1
    return odd_digit_seen(quotient)


def proof_summary(n):
    return odd_digits_product(n) * odd_digit_seen(n)


def oracle(n):
    odd_digits = [int(character) for character in str(n)
                  if int(character) % 2 == 1]
    if not odd_digits:
        return 0
    result = 1
    for digit in odd_digits:
        result *= digit
    return result


def main():
    inputs = list(range(1, 10001)) + [111111, 246802468, 975319753]
    mismatches = [
        (n, proof_summary(n), oracle(n))
        for n in inputs
        if proof_summary(n) != oracle(n)
    ]
    assert not mismatches, mismatches[:10]
    print(f"checked={len(inputs)} mismatches=0")


if __name__ == "__main__":
    main()
