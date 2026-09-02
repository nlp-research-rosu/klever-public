from solution import fizz_buzz


def arithmetic_model(n):
    total = 0
    for candidate in range(n):
        if candidate % 11 == 0 or candidate % 13 == 0:
            value = candidate
            while value > 0:
                total += value % 10 == 7
                value //= 10
    return total


def string_oracle(n):
    return sum(
        str(candidate).count("7")
        for candidate in range(n)
        if candidate % 11 == 0 or candidate % 13 == 0
    )


inputs = list(range(-25, 501)) + [777, 1000, 2026, 5000, 10000]
mismatches = []
for value in inputs:
    implementation = fizz_buzz(value)
    model = arithmetic_model(value)
    oracle = string_oracle(value)
    if not implementation == model == oracle:
        mismatches.append((value, implementation, model, oracle))

print(f"inputs={len(inputs)} mismatches={len(mismatches)}")
if mismatches:
    print(mismatches[:10])
    raise SystemExit(1)
