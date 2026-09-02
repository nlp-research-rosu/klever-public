#!/usr/bin/env python3
"""Append independent ground assertions to the exact submitted source body."""

from pathlib import Path


WORK = Path("/tmp/audit-work/125-split-words")
source = (WORK / "solution.py").read_text(encoding="utf-8")
tests = '''

assert split_words("Hello world!") == ["Hello", "world!"]
assert split_words(" ") == []
assert split_words(",") == ["", ""]
assert split_words("") == 0
'''
(WORK / "audit-ground-witnesses.py").write_text(source + tests, encoding="utf-8")
print("wrote=", WORK / "audit-ground-witnesses.py", sep="")
