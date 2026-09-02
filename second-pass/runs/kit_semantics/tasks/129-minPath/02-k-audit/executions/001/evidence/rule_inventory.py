#!/usr/bin/env python3
"""Exhaustive line-oriented inventory of K declarations, rules, and claims."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/129-minPath-audit")
KEYWORD = re.compile(
    r"^(?:(requires)(?=\s+\")|(module|endmodule)\b|  (imports|configuration|syntax|context|rule|claim)\b)"
)


def statements(path: Path):
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = KEYWORD.match(line)
        if match:
            starts.append((index, next(group for group in match.groups() if group)))
    for position, (start, keyword) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block = lines[start:end]
        while block and (not block[-1].strip() or block[-1].lstrip().startswith("//")):
            block.pop()
        yield start + 1, keyword, "\n".join(block)


def main() -> None:
    paths = [ROOT / "reference-semantics" / "semantics.k"]
    paths.extend(sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")))
    paths.extend([ROOT / "verification.k", ROOT / "spec.k"])
    counts: collections.Counter[str] = collections.Counter()
    attribute_counts: collections.Counter[str] = collections.Counter()
    file_counts: dict[Path, collections.Counter[str]] = {
        path: collections.Counter() for path in paths
    }
    records: list[tuple[Path, int, str, str]] = []
    for path in paths:
        for line, keyword, block in statements(path):
            counts[keyword] += 1
            file_counts[path][keyword] += 1
            if keyword == "syntax":
                if "function" in block:
                    attribute_counts["function_syntax"] += 1
                if "total" in block:
                    attribute_counts["total_syntax"] += 1
                if "functional" in block:
                    attribute_counts["functional_syntax"] += 1
                if "no-evaluators" in block or "symbol(" in block:
                    attribute_counts["opaque_or_symbol_syntax"] += 1
            if keyword == "rule":
                for attribute in (
                    "simplification", "concrete", "macro", "macro-rec",
                    "priority", "owise", "anywhere", "trusted",
                ):
                    if re.search(rf"\b{re.escape(attribute)}\b", block):
                        attribute_counts[f"rule_{attribute}"] += 1
                if "<k>" in block:
                    attribute_counts["rule_mentions_k_cell"] += 1
            records.append((path, line, keyword, block))

    print(f"files={len(paths)}")
    print(f"counts={dict(counts)}")
    print(f"attribute_counts={dict(attribute_counts)}")
    print(f"literal_trusted_occurrences={sum(p.read_text().count('[trusted]') for p in paths)}")
    print(f"records={len(records)}")
    print("per_file_counts=")
    for path in paths:
        print(f"  {path.relative_to(ROOT)}: {dict(file_counts[path])}")
    for number, (path, line, keyword, block) in enumerate(records, 1):
        relative = path.relative_to(ROOT)
        normalized = " ".join(part.strip() for part in block.splitlines())
        print(f"{number:04d} {relative}:{line} {keyword}: {normalized}")


if __name__ == "__main__":
    main()
