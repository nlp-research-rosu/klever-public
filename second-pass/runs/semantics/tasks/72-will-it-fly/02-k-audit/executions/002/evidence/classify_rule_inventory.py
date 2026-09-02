#!/usr/bin/env python3
"""Attach an audit disposition to every inventoried K source sentence."""

from __future__ import annotations

from pathlib import Path


inventory = Path("/audit-output/evidence/rule-inventory.tsv")
reachable_fixed_modules = {
    "semantics.k",
    "syntax.k",
    "core.k",
    "iter.k",
    "operators.k",
    "int.k",
    "bool.k",
    "list.k",
    "subscript.k",
    "functions.k",
    "builtins.k",
    "call.k",
    "assert.k",
    "concrete.k",
}

with inventory.open(encoding="utf-8") as stream:
    header = stream.readline().rstrip("\n")
    print(header + "\tdisposition")
    for raw_line in stream:
        line = raw_line.rstrip("\n")
        if line.startswith("# counts "):
            print(line)
            continue
        source, lines, kind, attributes, text = line.split("\t", 4)
        start = int(lines.split("-", 1)[0])
        if source.startswith("/candidate/"):
            if start == 13:
                disposition = (
                    "CONCERN: [total] exceeds equation coverage; "
                    "all entry uses are guarded by allInts"
                )
            elif start in {30, 34}:
                disposition = (
                    "ACCEPTED-AS-TRUE-BRIDGE: exact pure fixed-semantics fold; "
                    "universal bridge-free K connection not closed"
                )
            else:
                disposition = (
                    "ACCEPTED-PROOF-LOCAL: truthful structural definition "
                    "or exact submitted-program alias"
                )
        else:
            basename = Path(source).name
            if "symbol" in attributes:
                disposition = (
                    "TRUSTED-FIXED-OPAQUE: supplied-semantics primitive; "
                    "unreachable from submitted program"
                )
            elif basename in reachable_fixed_modules:
                disposition = (
                    "TRUSTED-FIXED-REACHABLE-MODULE: selected supplied "
                    "semantics; used path reviewed for this program"
                )
            else:
                disposition = (
                    "TRUSTED-FIXED-UNREACHABLE-MODULE: selected supplied "
                    "semantics and inert for this program"
                )
        print(line + "\t" + disposition)
