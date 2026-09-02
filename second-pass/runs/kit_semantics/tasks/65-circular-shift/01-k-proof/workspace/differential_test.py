from solution import circular_shift


def direct_two_slice_oracle(x, shift):
    digits = str(x)
    if shift > len(digits):
        return digits[::-1]
    split = len(digits) - shift
    return digits[split:] + digits[:split]


def main():
    xs = list(range(-200, 201)) + [10**20 + 123456789]
    shifts = range(-12, 30)
    checked = 0
    for x in xs:
        for shift in shifts:
            actual = circular_shift(x, shift)
            expected = direct_two_slice_oracle(x, shift)
            assert actual == expected, (x, shift, actual, expected)
            checked += 1
    print(f"differential: {checked} cases, 0 mismatches")


if __name__ == "__main__":
    main()
