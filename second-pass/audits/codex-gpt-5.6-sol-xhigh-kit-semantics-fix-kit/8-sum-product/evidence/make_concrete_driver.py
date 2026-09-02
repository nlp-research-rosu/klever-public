#!/usr/bin/env python3
"""Append reviewer assertions to the exact audited source in scratch."""

from pathlib import Path


SOURCE = Path("/tmp/audit-work/solution.py")
DRIVER = Path("/tmp/audit-work/concrete_cases.py")

ASSERTIONS = r'''

assert sum_product([]) == (0, 1)
assert sum_product([1, 2, 3, 4]) == (10, 24)
assert sum_product([0]) == (0, 0)
assert sum_product([-1]) == (-1, -1)
assert sum_product([-2, 3]) == (1, -6)
assert sum_product([-2, -3]) == (-5, 6)
assert sum_product([-2, 3, 0]) == (1, 0)
assert sum_product([100000000000000000000, -2]) == (99999999999999999998, -200000000000000000000)
'''


def main() -> int:
    source = SOURCE.read_text(encoding="utf-8")
    DRIVER.write_text(source + ASSERTIONS, encoding="utf-8")
    print(f"source={SOURCE}")
    print(f"driver={DRIVER}")
    print(f"source_prefix_byte_equal={DRIVER.read_bytes().startswith(SOURCE.read_bytes())}")
    print("assertion_count=8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
