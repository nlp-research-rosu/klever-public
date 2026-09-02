#!/usr/bin/env python3
"""Exhaustive line-oriented inventory of local K declarations and rules."""

from __future__ import annotations

import collections
import re
from pathlib import Path


FILES = [
    Path("/tmp/audit-work/proof145/semantic.k"),
    Path("/tmp/audit-work/proof145/verification.k"),
]


def collapsed(lines):
    return " ".join(part.strip() for part in lines if part.strip())


for path in FILES:
    lines = path.read_text(encoding="utf-8").splitlines()
    print(f"FILE: {path}")
    modules = []
    declarations = []
    rules = []
    configuration = None
    attributes = collections.Counter()
    index = 0
    while index < len(lines):
        stripped = lines[index].strip()
        if stripped.startswith("module "):
            modules.append((index + 1, stripped))
            index += 1
            continue
        if stripped.startswith("syntax "):
            start = index
            block = [lines[index]]
            index += 1
            while index < len(lines) and lines[index].lstrip().startswith("|"):
                block.append(lines[index])
                index += 1
            text = collapsed(block)
            declarations.append((start + 1, index, text))
            for attribute in re.findall(r"\[([^\]]+)\]", text):
                for item in attribute.split(","):
                    attributes[item.strip()] += 1
            continue
        if stripped == "configuration":
            start = index
            block = [lines[index]]
            index += 1
            while index < len(lines):
                block.append(lines[index])
                if lines[index].strip() == "</py>":
                    index += 1
                    break
                index += 1
            configuration = (start + 1, index, collapsed(block))
            continue
        if stripped.startswith("rule "):
            start = index
            block = [lines[index]]
            index += 1
            while index < len(lines):
                next_stripped = lines[index].strip()
                if (
                    next_stripped.startswith("rule ")
                    or next_stripped.startswith("syntax ")
                    or next_stripped.startswith("module ")
                    or next_stripped == "endmodule"
                ):
                    break
                if next_stripped and not next_stripped.startswith("//"):
                    block.append(lines[index])
                index += 1
            text = collapsed(block)
            rules.append((start + 1, start + len(block), text))
            for attribute in re.findall(r"\[([^\]]+)\]", text):
                for item in attribute.split(","):
                    attributes[item.strip()] += 1
            continue
        index += 1

    print(f"MODULE_COUNT: {len(modules)}")
    for number, (line, text) in enumerate(modules, 1):
        print(f"MODULE {number:02d} line={line}: {text}")
    print(f"SYNTAX_DECLARATION_COUNT: {len(declarations)}")
    for number, (start, end, text) in enumerate(declarations, 1):
        print(f"DECL {number:02d} lines={start}-{end}: {text}")
    if configuration:
        print(
            f"CONFIG lines={configuration[0]}-{configuration[1]}: "
            f"{configuration[2]}"
        )
    print(f"RULE_COUNT: {len(rules)}")
    for number, (start, end, text) in enumerate(rules, 1):
        print(f"RULE {number:02d} lines={start}-{end}: {text}")
    print(f"ATTRIBUTE_COUNTS: {dict(attributes)}")
    print(
        "SPECIAL_ATTRIBUTE_COUNTS: "
        + repr(
            {
                name: attributes[name]
                for name in (
                    "function",
                    "total",
                    "functional",
                    "simplification",
                    "concrete",
                    "priority",
                )
            }
        )
    )
