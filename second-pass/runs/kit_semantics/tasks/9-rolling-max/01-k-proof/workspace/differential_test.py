from itertools import product

from solution import rolling_max


def oracle(values):
    expected = []
    for end in range(1, len(values) + 1):
        expected.append(max(values[:end]))
    return expected


def main():
    cases = 0
    mismatches = 0
    for length in range(6):
        for values in product(range(-2, 3), repeat=length):
            case = list(values)
            cases += 1
            if rolling_max(case) != oracle(case):
                mismatches += 1
                print("mismatch", case, rolling_max(case), oracle(case))
    print(f"cases={cases} mismatches={mismatches}")
    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
