#!/usr/bin/env python3
"""Wrap the regenerated submitted module in a concrete Invoke term."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("module")
    parser.add_argument("output")
    values_group = parser.add_mutually_exclusive_group(required=True)
    values_group.add_argument("--values-json")
    values_group.add_argument("--range-length", type=int)
    parser.add_argument("--delimiter", required=True, type=int)
    args = parser.parse_args()

    values = (
        json.loads(args.values_json)
        if args.values_json is not None
        else list(range(args.range_length))
    )
    if not isinstance(values, list) or not all(type(value) is int for value in values):
        raise TypeError("--values-json must be a JSON list of integers")
    module = Path(args.module).read_text(encoding="utf-8").strip()
    rendered_values = ", ".join(str(value) for value in values)
    term = (
        "Invoke(\n"
        f"{module},\n"
        '  "intersperse",\n'
        f"  VList([{rendered_values}]), VInt({args.delimiter}))\n"
    )
    Path(args.output).write_text(term, encoding="utf-8")
    print(
        json.dumps(
            {
                "output": args.output,
                "input_length": len(values),
                "delimiter": args.delimiter,
                "first": values[:4],
                "last": values[-4:],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
