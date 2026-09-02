import random

from solution import count_nums


def signed_digit_sum_oracle(number):
    text = str(number)
    if text[0] == "-":
        return -int(text[1]) + sum(int(char) for char in text[2:])
    return sum(int(char) for char in text)


def count_nums_oracle(values):
    return sum(signed_digit_sum_oracle(value) > 0 for value in values)


def main():
    cases = [
        [],
        [-1, 11, -11],
        [1, 1, 2],
        [-123, -100, -19, 0, 10, 99],
        [-(10**50 - 1), 10**50 - 1, -10000000000000000001],
    ]

    # Exhaustive singleton coverage around all sign and decimal boundaries.
    cases.extend([[value] for value in range(-5000, 5001)])

    rng = random.Random(20260729)
    for _ in range(2000):
        size = rng.randrange(0, 21)
        cases.append(
            [rng.randrange(-(10**30), 10**30 + 1) for _ in range(size)]
        )

    mismatches = []
    decimal_contract_failures = []
    checked_values = 0
    for values in cases:
        expected = count_nums_oracle(values)
        actual = count_nums(values)
        if actual != expected:
            mismatches.append((values, expected, actual))

        for value in values:
            checked_values += 1
            magnitude_text = str(abs(value))
            if not magnitude_text or not all("0" <= char <= "9" for char in magnitude_text):
                decimal_contract_failures.append((value, magnitude_text))

    print(
        f"cases={len(cases)} values={checked_values} "
        f"mismatches={len(mismatches)} "
        f"decimal_contract_failures={len(decimal_contract_failures)}"
    )
    if mismatches:
        print("first mismatch:", mismatches[0])
    if decimal_contract_failures:
        print("first decimal contract failure:", decimal_contract_failures[0])

    assert not mismatches
    assert not decimal_contract_failures


if __name__ == "__main__":
    main()
