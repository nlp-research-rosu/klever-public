from solution import digits


def oracle(n):
    product = 1
    found = False
    for character in str(n):
        digit = int(character)
        if digit % 2 == 1:
            product *= digit
            found = True
    return product if found else 0


def main():
    inputs = list(range(1, 10001)) + [111111, 246802468, 975319753]
    mismatches = [
        (n, digits(n), oracle(n))
        for n in inputs
        if digits(n) != oracle(n)
    ]
    assert not mismatches, mismatches[:10]
    print(f"checked={len(inputs)} mismatches=0")


if __name__ == "__main__":
    main()
