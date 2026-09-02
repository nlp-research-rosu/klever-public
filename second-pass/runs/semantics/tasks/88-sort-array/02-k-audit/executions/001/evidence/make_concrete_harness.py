#!/usr/bin/env python3
"""Create a concrete K harness whose prefix is the exact submitted solution.py."""

from pathlib import Path


scratch = Path("/tmp/audit-work/88-sort-array")
solution = (scratch / "solution.py").read_text(encoding="utf-8")
tests = r'''

assert sort_array([]) == []
assert sort_array([5]) == [5]
assert sort_array([0]) == [0]
assert sort_array([0, 1]) == [0, 1]
assert sort_array([1, 1]) == [1, 1]
assert sort_array([2, 4, 3, 0, 1, 5]) == [0, 1, 2, 3, 4, 5]
assert sort_array([2, 4, 3, 0, 1, 5, 6]) == [6, 5, 4, 3, 2, 1, 0]
assert sort_array([3, 0, 2]) == [0, 2, 3]
assert sort_array([3, 0, 3]) == [3, 3, 0]
assert sort_array([3, 0, 4]) == [0, 3, 4]

original = [2, 4, 3, 0, 1, 5]
result = sort_array(original)
assert original == [2, 4, 3, 0, 1, 5]
assert result == [0, 1, 2, 3, 4, 5]
'''
(scratch / "reviewer-concrete.py").write_text(solution + tests, encoding="utf-8")
print(f"solution_prefix_bytes={len(solution.encode('utf-8'))}")
print(f"harness={scratch / 'reviewer-concrete.py'}")
