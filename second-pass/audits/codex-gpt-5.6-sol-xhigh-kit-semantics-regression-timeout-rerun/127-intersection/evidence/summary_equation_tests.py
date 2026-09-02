#!/usr/bin/env python3
"""Finite independent checks of the scanPrime equations and intent bridge."""


def py_mod(n, i):
    return ((n % i) + i) % i


def intended_scan(n, i, p):
    if not p:
        return False
    if i < 2 and i < n:
        return False
    if i >= n:
        return p
    cursor = i
    while cursor < n:
        if n % cursor == 0:
            return False
        cursor += 1
    return p


def main():
    checks = 0
    failures = []
    for n in range(-10, 101):
        for i in range(-5, 111):
            for p in (False, True):
                value = intended_scan(n, i, p)

                if not p:
                    checks += 1
                    if value is not False:
                        failures.append(("false-absorbing", n, i, p))

                if i < 2 and i < n:
                    checks += 1
                    if value is not False:
                        failures.append(("off-domain", n, i, p))

                if i >= n:
                    checks += 1
                    if value is not p:
                        failures.append(("base", n, i, p))

                if i >= 2 and i < n and py_mod(n, i) == 0:
                    checks += 1
                    if value is not False:
                        failures.append(("divisor", n, i, p))

                if i >= 2 and i < n and py_mod(n, i) != 0:
                    checks += 1
                    if intended_scan(n, i + 1, p) is not value:
                        failures.append(("fold", n, i, p))

    intent_checks = 0
    for n in range(-10, 1001):
        summary = intended_scan(n, 2, n > 1)
        expected_prime = n >= 2 and all(n % d for d in range(2, n))
        intent_checks += 1
        if summary != expected_prime:
            failures.append(("intent", n, summary, expected_prime))

    print(
        f"equation_checks={checks} intent_checks={intent_checks} "
        f"failures={len(failures)}"
    )
    if failures:
        print(f"first_failures={failures[:20]}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
