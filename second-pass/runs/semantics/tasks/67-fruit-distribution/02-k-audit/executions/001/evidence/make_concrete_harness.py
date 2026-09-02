#!/usr/bin/env python3
"""Build a concrete test harness by appending tests to the scratch solution source."""

from pathlib import Path


solution = Path("/tmp/audit-work/reconstruction/solution.py").read_text()
tests = """

assert fruit_distribution("5 apples and 6 oranges", 19) == 8
assert fruit_distribution("0 apples and 0 oranges", 0) == 0
assert fruit_distribution("0 apples and 7 oranges", 7) == 0
assert fruit_distribution("9 apples and 0 oranges", 9) == 0
assert fruit_distribution("9 apples and 7 oranges", 16) == 0
assert fruit_distribution("123 apples and 456 oranges", 1000) == 421
"""

print(solution.rstrip() + tests)
