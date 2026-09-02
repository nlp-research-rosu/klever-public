from solution import tri


def recurrence_oracle(n):
    result = [1]
    for i in range(1, n + 1):
        if i == 1:
            result.append(3)
        elif i % 2 == 0:
            result.append(1 + i // 2)
        else:
            result.append(
                result[i - 1] + result[i - 2] + (1 + (i + 1) // 2)
            )
    return result


mismatches = []
for n in range(101):
    actual = tri(n)
    expected = recurrence_oracle(n)
    if actual != expected:
        mismatches.append((n, actual, expected))

print("Differential domain: integers 0..100")
print("Oracle: forward evaluation of the prompt recurrence")
print(f"Mismatches: {len(mismatches)}")
if mismatches:
    raise AssertionError(mismatches[0])
