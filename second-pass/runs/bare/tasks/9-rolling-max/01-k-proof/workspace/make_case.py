#!/usr/bin/env python3
"""Wrap the exact generated solution.mpy term in semantic.k's Run harness."""

from pathlib import Path
import argparse


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("numbers", nargs="*", type=int)
    args = parser.parse_args()

    module = Path("solution.mpy").read_text(encoding="utf-8").strip()
    numbers = ", ".join(str(number) for number in args.numbers)
    print(f"Run(\n{module},\n[{numbers}])")


if __name__ == "__main__":
    main()
