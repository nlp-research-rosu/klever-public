#!/usr/bin/env python3
"""Create a source-located inventory of every K declaration, rule, and claim."""

from __future__ import annotations

from collections import Counter
import csv
import hashlib
from pathlib import Path
import re


ROOT = Path("/tmp/audit-work/scratch")
OUTPUT = Path("/audit-output/evidence/rule-inventory.tsv")
START = re.compile(r"^\s*(syntax|rule|claim|context|configuration)\b")
FLAGS = (
    "function",
    "total",
    "functional",
    "symbol",
    "no-evaluators",
    "priority",
    "simplification",
    "concrete",
    "owise",
    "strict",
    "seqstrict",
    "macro",
    "macro-rec",
)

# Source regions exercised by solution.mpy. Everything else remains part of the
# byte-identical supplied library, but is not reachable from this program.
USED_REGIONS: dict[str, tuple[tuple[int, int], ...]] = {
    "semantics/syntax.k": ((9, 61),),
    "semantics/core.k": (
        (13, 42),
        (49, 60),
        (124, 134),
        (152, 181),
        (183, 196),
        (208, 210),
        (213, 219),
    ),
    "semantics/iter.k": ((8, 8),),
    "semantics/str.k": ((8, 17), (25, 25)),
    "semantics/operators.k": ((15, 17),),
    "semantics/int.k": ((9, 13), (22, 27)),
    "semantics/controls.k": ((9, 23), (46, 54), (62, 74)),
    "semantics/functions.k": ((8, 20), (62, 90)),
    "semantics/call.k": ((18, 21), (69, 75)),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def records(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    current: list[str] = []
    current_line = 0
    current_kind = ""

    def emit():
        if not current:
            return None
        source_lines = [
            line.strip()
            for line in current
            if line.strip() and not line.lstrip().startswith("//")
        ]
        source = " ".join(source_lines)
        source = re.sub(r"\s+", " ", source)
        return (current_line, current_kind, source)

    for line_number, line in enumerate(lines, 1):
        match = START.match(line)
        if match:
            prior = emit()
            if prior:
                yield prior
            current = [line]
            current_line = line_number
            current_kind = match.group(1)
        elif current:
            if re.match(r"^\s*(?:endmodule|module\b)", line):
                prior = emit()
                if prior:
                    yield prior
                current = []
                current_line = 0
                current_kind = ""
            else:
                current.append(line)
    prior = emit()
    if prior:
        yield prior


def disposition(relative: str, line: int, kind: str) -> str:
    if relative == "verification.k":
        if kind == "syntax":
            return "proof-local-summary-declaration-reviewed"
        if line <= 35:
            return "proof-local-summary-equation-reviewed"
        return "proof-local-operational-bridge-reviewed"
    if relative == "spec.k":
        return "target-claim-adequacy-reviewed"
    short = relative.removeprefix("reference-semantics/")
    for start, end in USED_REGIONS.get(short, ()):
        if start <= line <= end:
            return "trusted-supplied-used-path-reviewed"
    return "trusted-supplied-unused-by-solution"


def main() -> int:
    paths = sorted((ROOT / "reference-semantics").rglob("*.k"))
    paths.extend([ROOT / "verification.k", ROOT / "spec.k"])
    rows = []
    file_hashes = []
    for path in paths:
        relative = str(path.relative_to(ROOT))
        file_hashes.append((relative, sha256(path)))
        for line, kind, source in records(path):
            found_flags = [
                flag
                for flag in FLAGS
                if re.search(rf"(?<![A-Za-z-]){re.escape(flag)}(?:\(|\b)", source)
            ]
            rows.append(
                {
                    "id": len(rows) + 1,
                    "file": relative,
                    "line": line,
                    "kind": kind,
                    "flags": ",".join(found_flags) or "-",
                    "disposition": disposition(relative, line, kind),
                    "source": source,
                }
            )

    with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=(
                "id",
                "file",
                "line",
                "kind",
                "flags",
                "disposition",
                "source",
            ),
            dialect="excel-tab",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"inventory_file={OUTPUT}")
    print(f"source_file_count={len(paths)}")
    print(f"record_count={len(rows)}")
    print("kind_counts=" + repr(dict(sorted(Counter(r["kind"] for r in rows).items()))))
    flag_counts = Counter()
    for row in rows:
        for flag in row["flags"].split(","):
            if flag != "-":
                flag_counts[flag] += 1
    print("flag_counts=" + repr(dict(sorted(flag_counts.items()))))
    print(
        "disposition_counts="
        + repr(dict(sorted(Counter(r["disposition"] for r in rows).items())))
    )
    print("\nOPAQUE_OR_SYMBOL_DECLARATIONS")
    for row in rows:
        if "symbol" in row["flags"] or "no-evaluators" in row["flags"]:
            print(f"{row['file']}:{row['line']}: {row['source']}")
    print("\nSOURCE_SHA256")
    for relative, digest in file_hashes:
        print(f"{digest}  {relative}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
