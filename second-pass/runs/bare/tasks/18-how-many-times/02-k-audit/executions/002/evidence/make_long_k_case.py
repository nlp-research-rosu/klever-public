#!/usr/bin/env python3
from pathlib import Path

solution = Path("/tmp/audit-work/src/solution.py").read_text()
target = Path("/tmp/audit-work/concrete-tests/long_recursion.py")
target.write_text(solution + "\n\nhow_many_times(" + repr("a" * 1000) + ", \"b\")\n")
print(f"WROTE {target} string_len=1000 substring='b'")
