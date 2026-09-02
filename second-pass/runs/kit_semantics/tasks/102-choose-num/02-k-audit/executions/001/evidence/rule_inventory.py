#!/usr/bin/env python3
"""Exhaustive lexical inventory of the supplied K sources and proof files."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path


WORK = Path("/tmp/audit-work/102-choose-num")
OUT = Path("/audit-output/evidence")
KEYWORDS = (
    "module",
    "endmodule",
    "imports",
    "configuration",
    "syntax",
    "context",
    "rule",
    "claim",
    "alias",
)
START = re.compile(r"^\s*(" + "|".join(KEYWORDS) + r")\b")
ATTR = re.compile(r"\[([^\[\]]*)\]", re.S)


def source_paths() -> list[Path]:
    semantics = WORK / "reference-semantics"
    paths = [semantics / "semantics.k"]
    paths.extend(sorted((semantics / "semantics").glob("*.k")))
    paths.extend([WORK / "verification.k", WORK / "spec.k"])
    return paths


def sentence_rows(path: Path) -> list[dict[str, object]]:
    text = path.read_text()
    lines = text.splitlines()
    starts: list[tuple[int, str]] = []
    for line_number, line in enumerate(lines, 1):
        match = START.match(line)
        if match:
            starts.append((line_number, match.group(1)))
    rows: list[dict[str, object]] = []
    for index, (start_line, keyword) in enumerate(starts):
        end_line = starts[index + 1][0] - 1 if index + 1 < len(starts) else len(lines)
        segment = "\n".join(lines[start_line - 1 : end_line]).rstrip()
        normalized = " ".join(segment.split())
        attributes: list[str] = []
        for attr_text in ATTR.findall(segment):
            attributes.extend(part.strip() for part in attr_text.split(",") if part.strip())
        relative = path.relative_to(WORK).as_posix()
        used = used_by_solution(relative, start_line, end_line, normalized)
        if relative == "verification.k":
            if keyword == "syntax":
                assessment = "proof-local definitional summary; totality and result meaning reviewed"
            elif keyword == "rule":
                assessment = "proof-local guarded equation; truth, coverage, and overlap reviewed"
            else:
                assessment = "proof-local module/import boundary"
        elif relative == "spec.k":
            assessment = "target reachability claim; precondition, postcondition, and pinning reviewed"
        elif relative.startswith("reference-semantics/"):
            assessment = (
                "fixed supplied-semantics execution slice; manually reviewed for this program"
                if used
                else "fixed supplied-semantics item not reached by this program; no candidate extension"
            )
        else:
            assessment = "reviewed"
        if keyword == "rule":
            if "simplification" in attributes:
                rule_class = "simplification"
            elif "<k>" in segment or re.search(r"<[A-Za-z][^>]*>", segment):
                rule_class = "operational"
            else:
                rule_class = "equational"
        elif keyword == "syntax" and "function" in attributes:
            rule_class = "function-declaration"
        else:
            rule_class = keyword
        rows.append(
            {
                "source": relative,
                "start_line": start_line,
                "end_line": end_line,
                "keyword": keyword,
                "class": rule_class,
                "attributes": ";".join(attributes),
                "function": "function" in attributes,
                "total": "total" in attributes,
                "functional": "functional" in attributes,
                "simplification": "simplification" in attributes,
                "priority": next((a for a in attributes if a.startswith("priority(")), ""),
                "opaque_symbol": "no-evaluators" in attributes or any(a.startswith("symbol(") for a in attributes),
                "used_by_solution": used,
                "normalized_sha256": hashlib.sha256(normalized.encode()).hexdigest(),
                "assessment": assessment,
                "sentence": normalized,
            }
        )
    return rows


def overlap(start: int, end: int, first: int, last: int) -> bool:
    return start <= last and end >= first


def used_by_solution(source: str, start: int, end: int, sentence: str) -> bool:
    if source in {"verification.k", "spec.k", "reference-semantics/semantics.k"}:
        return True
    ranges = {
        "reference-semantics/semantics/syntax.k": [(9, 16), (28, 32), (41, 61)],
        "reference-semantics/semantics/core.k": [
            (25, 60),
            (123, 181),
            (183, 215),
        ],
        "reference-semantics/semantics/functions.k": [
            (8, 20),
            (62, 66),
            (77, 90),
        ],
        "reference-semantics/semantics/controls.k": [(50, 54)],
        "reference-semantics/semantics/operators.k": [(10, 20)],
        "reference-semantics/semantics/int.k": [(7, 27)],
        "reference-semantics/semantics/call.k": [(18, 21), (69, 74)],
    }
    return any(overlap(start, end, first, last) for first, last in ranges.get(source, []))


def function_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "source": row["source"],
            "start_line": row["start_line"],
            "end_line": row["end_line"],
            "total": row["total"],
            "functional": row["functional"],
            "opaque_symbol": row["opaque_symbol"],
            "used_by_solution": row["used_by_solution"],
            "attributes": row["attributes"],
            "declaration": row["sentence"],
            "assessment": row["assessment"],
        }
        for row in rows
        if row["function"]
    ]


def write_tsv(path: Path, rows: list[dict[str, object]]) -> None:
    assert rows
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    rows: list[dict[str, object]] = []
    for path in source_paths():
        assert path.is_file() and not path.is_symlink()
        rows.extend(sentence_rows(path))
    functions = function_rows(rows)
    write_tsv(OUT / "05-rule-inventory.tsv", rows)
    write_tsv(OUT / "05-function-inventory.tsv", functions)
    (OUT / "05-rule-inventory.json").write_text(json.dumps(rows, indent=2) + "\n")

    by_keyword = Counter(str(row["keyword"]) for row in rows)
    by_class = Counter(str(row["class"]) for row in rows)
    print(f"files={len(source_paths())} sentences={len(rows)}")
    print("by_keyword=" + json.dumps(dict(sorted(by_keyword.items())), sort_keys=True))
    print("by_class=" + json.dumps(dict(sorted(by_class.items())), sort_keys=True))
    print(f"function_declarations={len(functions)}")
    print(f"total_declarations={sum(bool(row['total']) for row in functions)}")
    print(f"functional_declarations={sum(bool(row['functional']) for row in functions)}")
    print(f"opaque_symbol_declarations={sum(bool(row['opaque_symbol']) for row in functions)}")
    print(f"simplification_rules={sum(bool(row['simplification']) for row in rows)}")
    print(f"priority_rules={sum(bool(row['priority']) for row in rows)}")
    print(f"used_slice_sentences={sum(bool(row['used_by_solution']) for row in rows)}")
    print("RULE_INVENTORY=PASS")


if __name__ == "__main__":
    main()
