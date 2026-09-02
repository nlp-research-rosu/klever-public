from solution import string_sequence


def oracle(n: int) -> str:
    return " ".join(str(i) for i in range(n + 1))


def main() -> None:
    inputs = list(range(-25, 251)) + [999]
    mismatches = []
    for n in inputs:
        actual = string_sequence(n)
        expected = oracle(n)
        if actual != expected:
            mismatches.append((n, actual, expected))

    print(f"inputs={len(inputs)} range=-25..250 plus 999")
    print(f"mismatches={len(mismatches)}")
    if mismatches:
        for item in mismatches[:10]:
            print(item)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
