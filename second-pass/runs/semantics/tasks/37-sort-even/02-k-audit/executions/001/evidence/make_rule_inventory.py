#!/usr/bin/env python3
"""Create a complete declaration/rule index for the audited K source set."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path("/tmp/audit-work/37-sort-even-audit/reconstruction-fresh")
SEMANTICS = ROOT / "reference-semantics"
FILES = sorted(SEMANTICS.rglob("*.k")) + [ROOT / "verification.k", ROOT / "spec.k"]
OUT_JSON = Path("/audit-output/evidence/k-rule-inventory.json")
OUT_TEXT = Path("/audit-output/evidence/k-rule-inventory.txt")

START = re.compile(
    r"^\s{2}(configuration|syntax|context|rule|claim|alias)\b"
)
BOUNDARY = re.compile(
    r"^\s{2}(configuration|syntax|context|rule|claim|alias|imports|endmodule)\b"
)
ATTR_NAMES = (
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
)


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def extract(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))

    records = []
    for position, (start, kind) in enumerate(starts):
        next_start = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        end = next_start
        while end > start + 1:
            last = lines[end - 1]
            if last.strip() == "" or last.lstrip().startswith("//"):
                end -= 1
            else:
                break
        block = "\n".join(lines[start:end])
        attrs = [name for name in ATTR_NAMES if re.search(rf"\b{re.escape(name)}\b", block)]
        records.append(
            {
                "file": relative(path),
                "line_start": start + 1,
                "line_end": end,
                "kind": kind,
                "attributes": attrs,
                "text": block,
            }
        )
    return records


def main() -> int:
    records = [record for path in FILES for record in extract(path)]
    kind_counts = Counter(record["kind"] for record in records)
    attribute_counts = Counter(
        attribute for record in records for attribute in record["attributes"]
    )
    per_file = Counter(record["file"] for record in records)
    payload = {
        "root": str(ROOT),
        "files": [relative(path) for path in FILES],
        "file_count": len(FILES),
        "record_count": len(records),
        "kind_counts": dict(sorted(kind_counts.items())),
        "attribute_counts": dict(sorted(attribute_counts.items())),
        "per_file_counts": dict(sorted(per_file.items())),
        "records": records,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    output = [
        f"root={ROOT}",
        f"file_count={len(FILES)}",
        f"record_count={len(records)}",
        "kind_counts=" + json.dumps(dict(sorted(kind_counts.items())), sort_keys=True),
        "attribute_counts="
        + json.dumps(dict(sorted(attribute_counts.items())), sort_keys=True),
        "",
        "PER-FILE COUNTS",
    ]
    output.extend(f"{file}: {count}" for file, count in sorted(per_file.items()))
    output.append("")
    output.append("DECLARATIONS AND RULES")
    for number, record in enumerate(records, 1):
        flattened = " ".join(
            part.strip()
            for part in record["text"].splitlines()
            if part.strip() and not part.lstrip().startswith("//")
        )
        output.append(
            f"{number:04d} {record['file']}:{record['line_start']}-{record['line_end']} "
            f"{record['kind']} attrs={','.join(record['attributes']) or '-'} :: {flattened}"
        )
    OUT_TEXT.write_text("\n".join(output) + "\n", encoding="utf-8")
    print(f"files={len(FILES)}")
    print(f"records={len(records)}")
    print("kind_counts=" + json.dumps(dict(sorted(kind_counts.items()))))
    print("attribute_counts=" + json.dumps(dict(sorted(attribute_counts.items()))))
    print(f"json={OUT_JSON}")
    print(f"text={OUT_TEXT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
