#!/usr/bin/env python3
"""Ground substitutions for the entry and loop-summary claims."""

import importlib.util


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_prime


def prime_scan(n: int, divisor: int) -> bool:
    if divisor < 2:
        return False
    return all(n % d != 0 for d in range(divisor, n))


def prime_result(n: int) -> bool:
    return False if n < 2 else prime_scan(n, 2)


canonical = load("canonical_ground", "/reference/canonical.py")
generated = load("generated_ground", "/tmp/audit-work/prime31/solution.py")

for n in [-7, 1, 2, 3, 4, 6, 31]:
    formal = prime_result(n)
    c_value = canonical(n)
    g_value = generated(n)
    print(
        f"entry N={n}: primeResult={formal} "
        f"canonical={c_value} generated={g_value}"
    )
    assert formal == c_value == g_value

loop_states = [
    # (N, D, A): D is at a real loop head reachable from entry N.
    (2, 2, True),
    (4, 2, True),
    (5, 3, True),
    (6, 3, False),
]
for n, divisor, accumulator in loop_states:
    expected = accumulator and prime_scan(n, divisor)
    print(
        f"loop N={n} D={divisor} A={accumulator}: "
        f"A_and_primeScan={expected}"
    )

print("RESULT=PASS")
