#!/usr/bin/env python3
"""Emit a line-addressable inventory of all K declarations in the audit sources."""

from collections import Counter, defaultdict
from pathlib import Path
import re


ROOT = Path("/tmp/audit-work/fresh")
FILES = [
    ROOT / "reference-semantics" / "semantics.k",
    *sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(r"^\s*(configuration|context|syntax|rule|claim)\b")
BOUNDARY = re.compile(
    r"^\s*(configuration|context|syntax|rule|claim|module|endmodule|imports)\b"
)
ATTRS = (
    "function",
    "total",
    "functional",
    "symbol",
    "no-evaluators",
    "priority",
    "simplification",
    "owise",
    "concrete",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
)


def declarations(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    for index in starts:
        match = START.match(lines[index])
        assert match is not None
        end = index + 1
        while end < len(lines):
            if BOUNDARY.match(lines[end]):
                break
            if lines[end].lstrip().startswith("//") and not lines[end].startswith("    "):
                break
            end += 1
        text = " ".join(part.strip() for part in lines[index:end] if part.strip())
        yield index + 1, match.group(1), text


def main():
    counts = Counter()
    by_file = defaultdict(Counter)
    records = []
    for path in FILES:
        origin = (
            "candidate-proof"
            if path.name in {"verification.k", "spec.k"}
            else "trusted-supplied-semantics"
        )
        for line, kind, text in declarations(path):
            flags = [attr for attr in ATTRS if re.search(rf"\b{re.escape(attr)}\b", text)]
            category = kind
            if kind == "rule":
                if "simplification" in flags:
                    category = "simplification-rule"
                elif "priority" in flags:
                    category = "priority-rule"
                elif "concrete" in flags:
                    category = "concrete-rule"
                elif "owise" in flags:
                    category = "owise-rule"
                else:
                    category = "ordinary-rule"
            rel = str(path.relative_to(ROOT))
            records.append((rel, line, origin, category, ",".join(flags) or "-", text))
            counts[category] += 1
            by_file[rel][category] += 1

    print("INVENTORY_COLUMNS: file<TAB>line<TAB>origin<TAB>category<TAB>attributes<TAB>declaration")
    for record in records:
        print("\t".join(map(str, record)))

    print("INVENTORY_SUMMARY")
    print(f"TOTAL_DECLARATIONS\t{len(records)}")
    for category, count in sorted(counts.items()):
        print(f"CATEGORY\t{category}\t{count}")
    for rel, file_counts in sorted(by_file.items()):
        summary = ",".join(f"{key}={value}" for key, value in sorted(file_counts.items()))
        print(f"FILE\t{rel}\t{summary}")


if __name__ == "__main__":
    main()
