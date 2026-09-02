#!/usr/bin/env python3
"""Render the special subsets of the exhaustive K declaration inventory."""

from __future__ import annotations

import json
from pathlib import Path


data = json.loads(
    Path("/audit-output/evidence/k-rule-inventory.json").read_text(
        encoding="utf-8"
    )
)
declarations = data["declarations"]


def show(title: str, selected: list[dict[str, object]], full: bool) -> None:
    print(title)
    if not selected:
        print("(none)")
    for item in selected:
        print(
            f"ID={item['id']} {item['file']}:{item['line']} "
            f"{item['classification']} "
            f"attrs={','.join(item['attributes'])}"
        )
        text = str(item["text"])
        print(text if full else text.splitlines()[0])
        print("---")


show(
    "Proof-extension declarations:",
    [
        item
        for item in declarations
        if item["source_group"] == "proof-extension"
    ],
    True,
)
show(
    "Opaque/no-evaluator declarations:",
    [
        item
        for item in declarations
        if item["opaque_in_symbolic_backend"]
    ],
    False,
)
show(
    "Simplification declarations:",
    [
        item
        for item in declarations
        if item["classification"] == "simplification-rule"
    ],
    True,
)
show(
    "Functional-keyword declarations:",
    [
        item
        for item in declarations
        if "functional" in item["attributes"]
    ],
    False,
)
