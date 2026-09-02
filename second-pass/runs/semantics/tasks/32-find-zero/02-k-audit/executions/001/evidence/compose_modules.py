#!/usr/bin/env python3
"""Reviewer-authored composition of translated Module(...) statement lists."""

from pathlib import Path
import sys


def body(path: str) -> str:
    text = Path(path).read_text(encoding="utf-8").strip()
    if not (text.startswith("Module(") and text.endswith(")")):
        raise SystemExit(f"{path}: not a translated Module term")
    return text[len("Module("):-1].strip()


if len(sys.argv) < 3:
    raise SystemExit("usage: compose_modules.py MODULE1.mpy MODULE2.mpy [...]")

print("Module(")
for module_path in sys.argv[1:]:
    for line in body(module_path).splitlines():
        print(f"  {line}")
print(")")
