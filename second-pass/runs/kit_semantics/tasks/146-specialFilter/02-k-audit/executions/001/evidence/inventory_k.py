#!/usr/bin/env python3
"""Create a line-addressable inventory of K declarations and rules."""

from __future__ import annotations

import collections
import pathlib
import re
import sys


START = re.compile(
    r"^(?:"
    r"requires\b"
    r"|[ \t]{0,2}(?:module|endmodule|imports|syntax|configuration|rule|claim|context|priority)\b"
    r")"
)
KEYWORD = re.compile(
    r"^\s*(module|endmodule|imports|requires|syntax|configuration|rule|claim|context|priority)\b"
)
ATTRS = (
    "function",
    "functional",
    "total",
    "macro",
    "symbol",
    "no-evaluators",
    "simplification",
    "priority",
    "concrete",
    "symbolic",
    "preserves-definedness",
    "owise",
    "anywhere",
    "heat",
    "cool",
)


def records(path: pathlib.Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block = "\n".join(lines[start:end]).rstrip()
        keyword = KEYWORD.match(lines[start]).group(1)  # type: ignore[union-attr]
        yield keyword, start + 1, block


def main() -> int:
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} FILE_OR_DIR ...", file=sys.stderr)
        return 2
    paths: list[pathlib.Path] = []
    for raw in sys.argv[1:]:
        candidate = pathlib.Path(raw)
        if candidate.is_dir():
            paths.extend(sorted(candidate.rglob("*.k")))
        else:
            paths.append(candidate)

    counts: collections.Counter[str] = collections.Counter()
    attr_counts: collections.Counter[str] = collections.Counter()
    file_counts: dict[str, collections.Counter[str]] = {}
    file_attrs: dict[str, collections.Counter[str]] = {}
    for path in paths:
        local_counts: collections.Counter[str] = collections.Counter()
        local_attrs: collections.Counter[str] = collections.Counter()
        file_counts[str(path)] = local_counts
        file_attrs[str(path)] = local_attrs
        print(f"\n===== FILE {path} =====")
        for keyword, line, block in records(path):
            counts[keyword] += 1
            local_counts[keyword] += 1
            code_only = "\n".join(line.split("//", 1)[0] for line in block.splitlines())
            found_attrs = (
                [attr for attr in ATTRS if re.search(rf"\b{re.escape(attr)}\b", code_only)]
                if keyword in {"syntax", "rule", "claim", "context", "configuration"}
                else []
            )
            for attr in found_attrs:
                attr_counts[attr] += 1
                local_attrs[attr] += 1
            suffix = f" attrs={','.join(found_attrs)}" if found_attrs else ""
            print(f"\n--- {path}:{line} kind={keyword}{suffix} ---")
            print(block)

    print("\n===== SUMMARY =====")
    print("records " + " ".join(f"{key}={counts[key]}" for key in sorted(counts)))
    print("attributes " + " ".join(f"{key}={attr_counts[key]}" for key in sorted(attr_counts)))
    print("\nfile\tsyntax\trule\tclaim\tcontext\tconfiguration\tfunction\ttotal\tmacro\t"
          "no-evaluators\tpriority\tsimplification\tconcrete\tsymbolic")
    for path in paths:
        local_counts = file_counts[str(path)]
        local_attrs = file_attrs[str(path)]
        values = [
            str(path),
            str(local_counts["syntax"]),
            str(local_counts["rule"]),
            str(local_counts["claim"]),
            str(local_counts["context"]),
            str(local_counts["configuration"]),
            str(local_attrs["function"]),
            str(local_attrs["total"]),
            str(local_attrs["macro"]),
            str(local_attrs["no-evaluators"]),
            str(local_attrs["priority"]),
            str(local_attrs["simplification"]),
            str(local_attrs["concrete"]),
            str(local_attrs["symbolic"]),
        ]
        print("\t".join(values))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
