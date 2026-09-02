#!/usr/bin/env python3
"""Inventory declarations and rules in the mounted fixed semantics and proof."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/54-same-chars")
START = re.compile(
    r"^\s*(requires|module|imports|syntax|configuration|context|rule|claim|alias|endmodule)\b"
)
ATTRIBUTE = re.compile(
    r"\b(functional|function|total|simplification|concrete|priority|owise|"
    r"macro-rec|macro|no-evaluators|symbol)\b"
)
RELEVANT = re.compile(
    r"#loadAll|configuration|"
    r"\bFuncDef\(|\bReturn\(|\bAssign\(Name|"
    r"\bName\(|#look\(|builtinsScope|"
    r"\bCall\(|#callee\(|#evalArgs\(|#evalArgCont\(|"
    r"#applyK\(toCall\((?:closureVal|builtinV)|"
    r"#bindP\(|#endcall|#pop\b|frame\(|"
    r"\bappendVal\(|"
    r"applyBuiltin\(\"set\"|"
    r"\bCompare\(|applyCmp\(\"==\",\s*setV|"
    r"\bcodeIn\(|\bdedupCodes\(|\bdedupFrom\(|\bsnocCode\(|"
    r"\bsubsetCodes\(|\bsameSet\("
)


def source_files() -> list[Path]:
    semantics = [ROOT / "reference-semantics" / "semantics.k"]
    semantics.extend(sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")))
    return semantics + [ROOT / "verification.k", ROOT / "spec.k"]


def blocks(path: Path):
    lines = path.read_text().splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    for position, index in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        match = START.match(lines[index])
        assert match
        kind = match.group(1)
        block_lines = lines[index:end]
        while block_lines and (
            not block_lines[-1].strip() or block_lines[-1].lstrip().startswith("//")
        ):
            block_lines.pop()
        text = " ".join(line.strip() for line in block_lines)
        text = re.sub(r"\s+", " ", text).strip()
        yield index + 1, kind, text


def classify(path: Path, kind: str, text: str) -> tuple[str, str]:
    relative = path.relative_to(ROOT).as_posix()
    if relative == "spec.k" and kind == "claim":
        return "target_claim", "AUDIT_TARGET"
    if relative == "verification.k":
        return "proof_module", "NO_PROOF_LOCAL_EXTENSION"
    if kind in {"rule", "syntax", "configuration", "context"} and RELEVANT.search(text):
        return "fixed_dependency_slice", "MANUAL_REVIEW"
    return "fixed_not_reached", "TRUSTED_SUPPLIED_BASELINE_UNREACHED"


def inventory():
    rows = []
    for path in source_files():
        for line, kind, text in blocks(path):
            attrs = sorted(set(ATTRIBUTE.findall(text)))
            reachability, disposition = classify(path, kind, text)
            rows.append(
                {
                    "file": path.relative_to(ROOT).as_posix(),
                    "line": line,
                    "kind": kind,
                    "attributes": ",".join(attrs) if attrs else "-",
                    "reachability": reachability,
                    "disposition": disposition,
                    "text": text,
                }
            )
    return rows


def print_tsv(rows) -> None:
    columns = [
        "id",
        "file",
        "line",
        "kind",
        "attributes",
        "reachability",
        "disposition",
        "text",
    ]
    print("\t".join(columns))
    for index, row in enumerate(rows, 1):
        values = [
            str(index),
            row["file"],
            str(row["line"]),
            row["kind"],
            row["attributes"],
            row["reachability"],
            row["disposition"],
            row["text"].replace("\t", " "),
        ]
        print("\t".join(values))


def print_summary(rows) -> None:
    kinds = Counter(row["kind"] for row in rows)
    dispositions = Counter(row["disposition"] for row in rows)
    attrs = Counter(
        attribute
        for row in rows
        for attribute in row["attributes"].split(",")
        if attribute != "-"
    )
    files = Counter(row["file"] for row in rows)
    print(f"inventory_rows={len(rows)}")
    print(f"kinds={dict(sorted(kinds.items()))}")
    print(f"attributes={dict(sorted(attrs.items()))}")
    print(f"dispositions={dict(sorted(dispositions.items()))}")
    print("per_file:")
    for file, count in sorted(files.items()):
        print(f"  {file}: {count}")
    relevant = [row for row in rows if row["disposition"] == "MANUAL_REVIEW"]
    print(f"manual_dependency_slice_rows={len(relevant)}")
    for row in relevant:
        excerpt = row["text"][:240]
        print(f"  {row['file']}:{row['line']} {row['kind']} {excerpt}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    rows = inventory()
    if args.summary:
        print_summary(rows)
    else:
        print_tsv(rows)


if __name__ == "__main__":
    main()
