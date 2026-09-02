from itertools import combinations, product

from solution import has_close_elements


def oracle(numbers, threshold):
    return any(abs(left - right) < threshold
               for left, right in combinations(numbers, 2))


def main():
    values = [-2.0, -0.5, 0.0, 0.5, 2.0]
    thresholds = [-1.0, 0.0, 0.25, 0.5, 1.0, 3.0]
    checked = 0
    mismatches = 0
    for size in range(5):
        for numbers in product(values, repeat=size):
            for threshold in thresholds:
                expected = oracle(numbers, threshold)
                actual = has_close_elements(list(numbers), threshold)
                checked += 1
                if actual != expected:
                    mismatches += 1
                    print("MISMATCH", numbers, threshold, expected, actual)
    print("checked:", checked)
    print("mismatches:", mismatches)
    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
