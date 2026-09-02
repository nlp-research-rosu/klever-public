#!/usr/bin/env python3
"""Exhaustive source-level declaration/rule inventory for the audit."""

from __future__ import annotations

import collections
import hashlib
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/8-sum-product")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(
    r"^\s*(module|endmodule|imports|configuration|syntax|context|rule|claim|alias)\b"
)
INVENTORIED = {"configuration", "syntax", "context", "rule", "claim", "alias"}


def normalized(lines: list[str]) -> str:
    pieces = []
    for line in lines:
        content = line.split("//", 1)[0].strip()
        if content:
            pieces.append(content)
    return " ".join(pieces)


entries: list[dict[str, object]] = []
file_hashes = []
for path in FILES:
    relative = path.relative_to(ROOT).as_posix()
    data = path.read_bytes()
    file_hashes.append((relative, hashlib.sha256(data).hexdigest()))
    lines = data.decode().splitlines()
    current_kind = None
    current_line = None
    current_lines: list[str] = []
    current_module = ""

    def finish() -> None:
        global current_kind, current_line, current_lines, current_module
        if current_kind is None:
            return
        statement = normalized(current_lines)
        if current_kind == "module":
            match = re.match(r"module\s+([A-Za-z0-9_-]+)", statement)
            if match:
                current_module = match.group(1)
        if current_kind in INVENTORIED:
            attributes = []
            for match in re.finditer(r"\[([^\]]*)\]", statement):
                attributes.extend(
                    part.strip() for part in match.group(1).split(",") if part.strip()
                )
            lowered_attributes = " ".join(attributes).lower()
            flags = []
            if current_kind == "syntax" and statement.startswith("syntax priorities"):
                flags.append("priority-declaration")
            if current_kind == "syntax" and "function" in lowered_attributes:
                flags.append("function")
            if current_kind == "syntax" and "total" in lowered_attributes:
                flags.append("total")
            if current_kind == "syntax" and "functional" in lowered_attributes:
                flags.append("functional")
            if current_kind == "syntax" and (
                "no-evaluators" in lowered_attributes or "symbol(" in lowered_attributes
            ):
                flags.append("opaque-or-symbol")
            if current_kind == "rule":
                if "simplification" in lowered_attributes:
                    flags.append("simplification")
                else:
                    flags.append("ordinary-semantic")
                if "priority" in lowered_attributes:
                    flags.append("priority-rule")
                if "macro" in lowered_attributes:
                    flags.append("macro")
                if "anywhere" in lowered_attributes:
                    flags.append("anywhere")
            if current_kind == "claim":
                flags.append("reachability-claim")
            baseline = relative.startswith("reference-semantics/")
            entries.append(
                {
                    "file": relative,
                    "line": current_line,
                    "module": current_module,
                    "kind": current_kind,
                    "flags": ",".join(flags) if flags else "-",
                    "authority": (
                        "fixed-supplied-semantics"
                        if baseline
                        else "candidate-proof-local"
                    ),
                    "statement": statement,
                }
            )
        current_kind = None
        current_line = None
        current_lines = []

    for line_number, line in enumerate(lines, 1):
        match = START.match(line)
        if match:
            finish()
            current_kind = match.group(1)
            current_line = line_number
            current_lines = [line]
        elif current_kind is not None:
            current_lines.append(line)
    finish()

print(f"FILES={len(FILES)}")
print(f"ENTRIES={len(entries)}")
counts = collections.Counter(str(entry["kind"]) for entry in entries)
flag_counts = collections.Counter()
authority_counts = collections.Counter(str(entry["authority"]) for entry in entries)
per_file_counts: dict[str, collections.Counter[str]] = {}
for entry in entries:
    per_file_counts.setdefault(
        str(entry["file"]), collections.Counter()
    )[str(entry["kind"])] += 1
    if entry["flags"] != "-":
        flag_counts.update(str(entry["flags"]).split(","))
print("KIND_COUNTS=" + repr(dict(sorted(counts.items()))))
print("FLAG_COUNTS=" + repr(dict(sorted(flag_counts.items()))))
print("AUTHORITY_COUNTS=" + repr(dict(sorted(authority_counts.items()))))
print("PER_FILE_COUNTS")
for relative, file_counts in sorted(per_file_counts.items()):
    print(f"  {relative}\t{dict(sorted(file_counts.items()))}")
print("SOURCE_FILE_HASHES")
for relative, digest in file_hashes:
    print(f"  {relative}\t{digest}")
print("INVENTORY_TSV")
print("id\tfile\tline\tmodule\tkind\tflags\tauthority\tstatement")
for identifier, entry in enumerate(entries, 1):
    statement = str(entry["statement"]).replace("\t", " ")
    print(
        f"{identifier}\t{entry['file']}\t{entry['line']}\t{entry['module']}\t"
        f"{entry['kind']}\t{entry['flags']}\t{entry['authority']}\t{statement}"
    )
