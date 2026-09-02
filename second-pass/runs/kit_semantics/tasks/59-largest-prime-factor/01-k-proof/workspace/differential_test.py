from solution import largest_prime_factor


def is_prime(candidate):
    if candidate < 2:
        return False
    divisor = 2
    while divisor * divisor <= candidate:
        if candidate % divisor == 0:
            return False
        divisor += 1
    return True


def oracle(n):
    answer = 1
    candidate = 2
    while candidate <= n:
        if n % candidate == 0 and is_prime(candidate):
            answer = candidate
        candidate += 1
    return answer


def is_composite(n):
    return n > 1 and not is_prime(n)


inputs = [n for n in range(2, 5001) if is_composite(n)]
inputs.extend([13195])
mismatches = []

for n in inputs:
    actual = largest_prime_factor(n)
    expected = oracle(n)
    if actual != expected:
        mismatches.append((n, actual, expected))

print(f"cases={len(inputs)} mismatches={len(mismatches)}")
if mismatches:
    print(mismatches[:10])
    raise SystemExit(1)
