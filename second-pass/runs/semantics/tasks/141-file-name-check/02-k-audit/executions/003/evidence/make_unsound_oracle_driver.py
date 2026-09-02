#!/usr/bin/env python3
"""Build a concrete driver showing all false-conclusion filenames are valid."""

from pathlib import Path


SOURCE = Path("/tmp/audit-work/reconstruction/solution.py")
OUTPUT = Path("/tmp/audit-work/reconstruction/unsound_oracle_driver.py")

ASSERTIONS = r'''

assert file_name_check("a.txt") == "Yes"
assert file_name_check("b.txt") == "Yes"
assert file_name_check("c.txt") == "Yes"
assert file_name_check("d.txt") == "Yes"
assert file_name_check("e.exe") == "Yes"
assert file_name_check("f.dll") == "Yes"
'''


def main() -> None:
    OUTPUT.write_text(
        SOURCE.read_text(encoding="utf-8").rstrip() + ASSERTIONS,
        encoding="utf-8",
    )
    print(f"source={SOURCE}")
    print(f"output={OUTPUT}")
    print("expected=all six calls return Yes")


if __name__ == "__main__":
    main()
