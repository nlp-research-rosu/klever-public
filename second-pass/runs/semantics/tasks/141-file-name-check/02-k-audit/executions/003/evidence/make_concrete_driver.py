#!/usr/bin/env python3
"""Append independent concrete assertions to the exact submitted solution."""

from pathlib import Path


SOURCE = Path("/tmp/audit-work/reconstruction/solution.py")
OUTPUT = Path("/tmp/audit-work/reconstruction/concrete_audit.py")

ASSERTIONS = r'''

assert file_name_check("") == "No"
assert file_name_check("example.txt") == "Yes"
assert file_name_check("1example.dll") == "No"
assert file_name_check(".txt") == "No"
assert file_name_check("a.tx") == "No"
assert file_name_check("a.txt") == "Yes"
assert file_name_check("A.exe") == "Yes"
assert file_name_check("z.dll") == "Yes"
assert file_name_check("@.txt") == "No"
assert file_name_check("[.txt") == "No"
assert file_name_check("`.txt") == "No"
assert file_name_check("{.txt") == "No"
assert file_name_check("a.bin") == "No"
assert file_name_check("a.TXT") == "No"
assert file_name_check("a..txt") == "No"
assert file_name_check("a123.txt") == "Yes"
assert file_name_check("a1234.txt") == "No"
assert file_name_check("a0b1c2.dll") == "Yes"
assert file_name_check("a0b1c2d3.dll") == "No"
'''


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    OUTPUT.write_text(source.rstrip() + ASSERTIONS, encoding="utf-8")
    print(f"source={SOURCE}")
    print(f"output={OUTPUT}")
    print(f"assertion_count={ASSERTIONS.count('assert ')}")


if __name__ == "__main__":
    main()
