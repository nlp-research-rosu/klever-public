#!/usr/bin/env python3
"""Create a fresh, result-constraining false mutation of SPEC.top-correct."""

from __future__ import annotations

import argparse
from pathlib import Path


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"expected one occurrence of {old!r}, found {count}")
    return text.replace(old, new)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    text = args.source.read_text(encoding="utf-8")
    text = replace_once(text, "module SPEC\n", "module SPEC-VACUITY-AUDIT\n")
    text = replace_once(
        text,
        "        => pyList(sortEvenReference(L))\n",
        "        => pyList(ListItem(0) sortEvenReference(L))\n",
    )
    text = replace_once(
        text, "[label(top-correct)]", "[label(top-false-leading-zero)]"
    )
    args.output.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
