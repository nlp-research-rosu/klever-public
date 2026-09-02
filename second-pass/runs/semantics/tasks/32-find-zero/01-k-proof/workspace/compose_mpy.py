#!/usr/bin/env python3
"""Compose the statements of two translated Module(...) terms."""

from pathlib import Path
import sys


def module_body(path: str) -> str:
    text = Path(path).read_text(encoding="utf-8").strip()
    if not text.startswith("Module(") or not text.endswith(")"):
        raise SystemExit(f"{path}: expected a Module(...) term")
    return text[len("Module("):-1].strip()


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: compose_mpy.py PROGRAM.mpy CALLS.mpy")
    bodies = [module_body(path) for path in sys.argv[1:]]
    print("Module(")
    for body in bodies:
        if body:
            for line in body.splitlines():
                print(f"  {line}")
    print(")")


if __name__ == "__main__":
    main()
