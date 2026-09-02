from itertools import product

from solution import monotonic


def adjacent_pair_oracle(values):
    nondecreasing = all(
        values[index] <= values[index + 1]
        for index in range(len(values) - 1)
    )
    nonincreasing = all(
        values[index] >= values[index + 1]
        for index in range(len(values) - 1)
    )
    return nondecreasing or nonincreasing


def main():
    checked = 0
    mismatches = 0
    for length in range(7):
        for values in product(range(-3, 4), repeat=length):
            values = list(values)
            checked += 1
            if monotonic(values) != adjacent_pair_oracle(values):
                mismatches += 1
                print("mismatch:", values)
    print(f"checked={checked} mismatches={mismatches}")
    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
