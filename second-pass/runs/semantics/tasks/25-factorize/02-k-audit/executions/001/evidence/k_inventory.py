#!/usr/bin/env python3
"""Emit a complete declaration/rule inventory for the audited K sources."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path("/tmp/audit-work/25-factorize-audit")
SOURCES = [
    ROOT / "reference-semantics" / "semantics.k",
    *sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]

START = re.compile(
    r"^(?:(requires|module|endmodule)\b|"
    r"\s{2}(imports|syntax|configuration|context(?:\s+alias)?|rule|claim)\b)"
)
ATTRS = (
    "function",
    "total",
    "functional",
    "symbol",
    "no-evaluators",
    "concrete",
    "simplification",
    "priority",
    "owise",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
)


def kind(line: str) -> str:
    match = START.match(line)
    assert match is not None
    token = match.group(1) or match.group(2)
    return "context" if token.startswith("context") else token


def main() -> int:
    records: list[tuple[Path, int, int, str, str]] = []
    per_file: dict[str, Counter[str]] = defaultdict(Counter)
    attr_counts: Counter[str] = Counter()

    for path in SOURCES:
        lines = path.read_text(encoding="utf-8").splitlines()
        starts = [index for index, line in enumerate(lines) if START.match(line)]
        for position, start in enumerate(starts):
            end = starts[position + 1] if position + 1 < len(starts) else len(lines)
            record_lines = lines[start:end]
            while record_lines and (
                not record_lines[-1].strip()
                or record_lines[-1].lstrip().startswith("//")
            ):
                record_lines.pop()
            text = "\n".join(record_lines)
            record_kind = kind(lines[start])
            relative = path.relative_to(ROOT)
            records.append((relative, start + 1, start + len(record_lines), record_kind, text))
            per_file[str(relative)][record_kind] += 1
            for attr in ATTRS:
                if re.search(rf"\b{re.escape(attr)}\b", text):
                    attr_counts[attr] += 1

    print("INVENTORY_FORMAT=complete declaration blocks beginning with "
          "requires/module/imports/syntax/configuration/context/rule/claim/endmodule")
    print(f"SOURCE_FILE_COUNT={len(SOURCES)}")
    print(f"RECORD_COUNT={len(records)}")
    print("ATTRIBUTE_RECORD_COUNTS=" + ",".join(
        f"{name}:{attr_counts[name]}" for name in ATTRS
    ))
    print("--- PER_FILE_COUNTS ---")
    for filename in sorted(per_file):
        rendered = ",".join(
            f"{record_kind}:{count}"
            for record_kind, count in sorted(per_file[filename].items())
        )
        print(f"{filename}\t{rendered}")

    print("--- COMPLETE_RECORDS ---")
    for ordinal, (path, start, end, record_kind, text) in enumerate(records, 1):
        attrs = [attr for attr in ATTRS if re.search(rf"\b{re.escape(attr)}\b", text)]
        print(
            f"@@ RECORD {ordinal:04d} {path}:{start}-{end} "
            f"KIND={record_kind} ATTRS={','.join(attrs) or '-'}"
        )
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
