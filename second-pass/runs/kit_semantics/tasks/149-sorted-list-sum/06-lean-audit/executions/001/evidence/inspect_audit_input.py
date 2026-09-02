#!/usr/bin/env python3
"""Print the launcher audit-input structure without executing mounted content."""

from __future__ import annotations

import json
from pathlib import Path


def describe(value: object, prefix: str = "") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            path = f"{prefix}.{key}" if prefix else key
            if isinstance(child, dict):
                print(f"{path}: object[{len(child)}]")
                describe(child, path)
            elif isinstance(child, list):
                print(f"{path}: list[{len(child)}]")
            else:
                print(f"{path}: {child!r}")


describe(json.loads(Path("/audit-input.json").read_text()))
