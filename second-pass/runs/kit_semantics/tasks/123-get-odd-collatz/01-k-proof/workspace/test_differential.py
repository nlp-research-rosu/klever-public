from solution import get_odd_collatz


def oracle(n):
    odd_values = []
    current = n
    while True:
        if current % 2 == 1:
            odd_values.append(current)
        if current == 1:
            return sorted(odd_values)
        if current % 2 == 0:
            current //= 2
        else:
            current = 3 * current + 1


def main():
    inputs = list(range(1, 201)) + [255, 256, 257, 511, 512, 513, 1024]
    mismatches = []
    for n in inputs:
        actual = get_odd_collatz(n)
        expected = oracle(n)
        if actual != expected:
            mismatches.append((n, actual, expected))
    print(f"checked={len(inputs)} mismatches={len(mismatches)}")
    if mismatches:
        print(mismatches[:3])
        raise SystemExit(1)


if __name__ == "__main__":
    main()
