#!/usr/bin/env python3
"""Build a concrete K smoke program from the exact scratch solution source."""
from pathlib import Path

source = Path("/tmp/audit-work/case/solution.py").read_text(encoding="utf-8")
tests = """

# Reviewer-authored normal and boundary executions.
assert has_close_elements([1.0, 2.0, 3.0], 0.5) == False
assert has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3) == True
assert has_close_elements([], 1.0) == False
assert has_close_elements([1.0], 1.0) == False
assert has_close_elements([1.0, 1.5], 0.5) == False
assert has_close_elements([1.0, 1.5], 0.5000000000000001) == True
assert has_close_elements([7.0, 7.0], 0.0) == False
assert has_close_elements([7.0, 7.0], 0.000001) == True
assert has_close_elements([-4.0, -4.25, 10.0], 0.3) == True
assert has_close_elements([0.0, 10.0, 20.0, 20.1], 0.2) == True
assert has_close_elements([1.0, 100.0, 1.1], 0.2) == True
assert has_close_elements([1.0, 1.0], -0.1) == False
"""
Path("/tmp/audit-work/case/concrete-audit.py").write_text(
    source.rstrip() + "\n" + tests,
    encoding="utf-8",
)
