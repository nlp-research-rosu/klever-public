from itertools import product

from solution import is_equal_to_sum_even


def main():
    positive_evens = range(2, 102, 2)
    representable = {
        a + b + c + d
        for a, b, c, d in product(positive_evens, repeat=4)
    }
    inputs = range(-20, 101)
    mismatches = [
        n
        for n in inputs
        if is_equal_to_sum_even(n) != (n in representable)
    ]
    print(f"checked={len(inputs)} mismatches={len(mismatches)}")
    if mismatches:
        print(mismatches)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
