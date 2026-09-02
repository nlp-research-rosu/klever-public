#!/usr/bin/env python3
"""Exhaustive top-level K declaration inventory for the audited definition."""

from __future__ import annotations

import collections
import glob
import re
from pathlib import Path


paths = [Path("/tmp/audit-work/162-string-to-md5/reference-semantics/semantics.k")]
paths += [
    Path(path)
    for path in sorted(
        glob.glob(
            "/tmp/audit-work/162-string-to-md5/reference-semantics/semantics/*.k"
        )
    )
]
paths += [
    Path("/tmp/audit-work/162-string-to-md5/verification.k"),
    Path("/tmp/audit-work/162-string-to-md5/spec.k"),
]

start_re = re.compile(
    r'^(?:(requires)\s+"|(module)\b|(endmodule)\b|  (imports|configuration|syntax|rule|context|claim)\b)'
)
attribute_names = (
    "function",
    "total",
    "functional",
    "symbol",
    "no-evaluators",
    "simplification",
    "concrete",
    "priority",
    "owise",
    "strict",
    "seqstrict",
    "macro",
)
counts: collections.Counter[str] = collections.Counter()
file_counts: dict[str, collections.Counter[str]] = {}
blocks: list[tuple[Path, int, int, str, str, tuple[str, ...]]] = []
all_rule_text = ""

for path in paths:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = start_re.match(line)
        if match:
            kind = next(group for group in match.groups() if group is not None)
            starts.append((index, kind))
    per_file: collections.Counter[str] = collections.Counter()
    for start_index, (line_index, kind) in enumerate(starts):
        next_line = starts[start_index + 1][0] if start_index + 1 < len(starts) else len(lines)
        # Do not absorb trailing comments/blank lines into the declaration text.
        end_index = next_line
        while end_index > line_index + 1 and (
            not lines[end_index - 1].strip()
            or lines[end_index - 1].lstrip().startswith("//")
        ):
            end_index -= 1
        text = "\n".join(lines[line_index:end_index]).rstrip()
        attribute_text = ",".join(re.findall(r"\[([^\]]+)\]", text))
        attrs = tuple(
            name
            for name in attribute_names
            if re.search(
                rf"(?<![A-Za-z0-9-]){re.escape(name)}(?![A-Za-z0-9-])",
                attribute_text,
            )
        )
        blocks.append((path, line_index + 1, end_index, kind, text, attrs))
        counts[kind] += 1
        per_file[kind] += 1
        if kind == "rule":
            all_rule_text += "\n" + text
    file_counts[str(path)] = per_file

print("COMMAND: python3 /audit-output/evidence/stage5_inventory.py")
print(f"FILES={len(paths)}")
print(f"TOP_LEVEL_DECLARATIONS={len(blocks)}")
print("COUNTS=" + " ".join(f"{key}={counts[key]}" for key in sorted(counts)))
print()
print("== Per-file counts ==")
for path in paths:
    counter = file_counts[str(path)]
    print(
        f"{path}: "
        + " ".join(f"{key}={counter[key]}" for key in sorted(counter))
    )

print()
print("== Every top-level declaration/rule ==")

program_ranges = {
    "core.k": [(13, 60), (124, 205), (238, 244)],
    "float.k": [(58, 61)],
    "operators.k": [(14, 20)],
    "str.k": [(12, 26)],
    "controls.k": [(8, 18), (50, 54)],
    "functions.k": [(8, 20), (62, 90)],
    "call.k": [(15, 24), (69, 75)],
    "methods.k": [(9, 10), (57, 58)],
    "builtins.k": [(320, 329)],
    "syntax.k": [(9, 61)],
}
boundary_ranges = {
    "float.k": [(58, 61, "SUPPLIED_IMPORT_BINDING_BOUNDARY")],
    "methods.k": [(57, 58, "SUPPLIED_ENCODING_BOUNDARY")],
    "builtins.k": [(320, 329, "SUPPLIED_MD5_BOUNDARY")],
}


def disposition(path: Path, start: int, end: int, kind: str, attrs: tuple[str, ...]) -> str:
    if path.name == "verification.k":
        return "CANDIDATE_WRAPPER_NO_EXTENSION"
    if path.name == "spec.k":
        return "TARGET_CLAIM" if kind == "claim" else "SPEC_STRUCTURE"
    if path.name == "semantics.k":
        return "FIXED_DEFINITION_ASSEMBLY"
    for low, high, boundary in boundary_ranges.get(path.name, []):
        if start <= high and end >= low:
            return boundary
    for low, high in program_ranges.get(path.name, []):
        if start <= high and end >= low:
            return "EXACT_PROGRAM_PATH"
    if "no-evaluators" in attrs:
        return "UNREACHED_FIXED_OPAQUE"
    if kind in {"rule", "context", "syntax", "configuration"}:
        return "UNREACHED_FIXED_DECLARATION"
    return "FIXED_MODULE_STRUCTURE"


for ordinal, (path, start, end, kind, block, attrs) in enumerate(blocks, 1):
    source = "SUPPLIED_FIXED" if "reference-semantics" in str(path) else "CANDIDATE"
    review_disposition = disposition(path, start, end, kind, attrs)
    flattened = " ".join(block.split())
    print(
        f"INV-{ordinal:04d} SOURCE={source} KIND={kind} "
        f"FILE={path} LINES={start}-{end} "
        f"ATTRS={','.join(attrs) or '-'} DISPOSITION={review_disposition}"
    )
    print("  " + flattened)

print()
print("== Function-like declaration coverage heuristic ==")
function_symbols: set[str] = set()
for _path, _start, _end, kind, block, _attrs in blocks:
    if kind != "syntax" or "[function" not in block:
        continue
    for symbol in re.findall(r"\b([A-Za-z#][A-Za-z0-9#]*)\s*\([^)]*\)\s*\[function", block):
        function_symbols.add(symbol)
for symbol in sorted(function_symbols):
    direct_rule = re.search(rf"\brule\s+{re.escape(symbol)}\s*\(", all_rule_text) is not None
    print(f"FUNCTION_SYMBOL={symbol} HAS_DIRECT_RULE={str(direct_rule).lower()}")

print()
print("== Attribute totals over declaration blocks ==")
for attribute in attribute_names:
    total = sum(attribute in attrs for *_prefix, attrs in blocks)
    print(f"ATTRIBUTE={attribute} BLOCKS={total}")
