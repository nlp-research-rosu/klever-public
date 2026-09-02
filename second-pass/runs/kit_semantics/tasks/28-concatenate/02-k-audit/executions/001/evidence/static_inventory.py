#!/usr/bin/env python3
"""Generate an exhaustive declaration/rule inventory for the audited K sources."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOTS = [
    Path("/reference/reference-semantics/semantics.k"),
    *sorted(Path("/reference/reference-semantics/semantics").glob("*.k")),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]
OUTPUT = Path("/audit-output/evidence/stage5-rule-inventory.tsv")
START = re.compile(
    r'^(?:(requires)\s+"|(module|endmodule)\b| {2}(imports|configuration|syntax|rule|claim|context|alias)\b)'
)


def records(path: Path) -> list[dict[str, object]]:
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            kind = next(group for group in match.groups() if group is not None)
            starts.append((index, kind))
    out: list[dict[str, object]] = []
    for pos, (index, kind) in enumerate(starts):
        end = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        block_lines = lines[index:end]
        while block_lines and not block_lines[-1].strip():
            block_lines.pop()
        while block_lines and block_lines[-1].lstrip().startswith("//"):
            block_lines.pop()
        block = " ".join(part.strip() for part in block_lines if part.strip())
        code_only = " ".join(part.split("//", 1)[0].strip() for part in block_lines if part.strip())
        attributes = sorted(set(re.findall(r"\[([^\]]+)\]", code_only)))
        flags = []
        for flag in [
            "function",
            "functional",
            "total",
            "symbol",
            "no-evaluators",
            "macro",
            "strict",
            "seqstrict",
            "priority",
            "owise",
            "simplification",
            "concrete",
            "anywhere",
        ]:
            if re.search(rf"\b{re.escape(flag)}\b", code_only):
                flags.append(flag)
        label_match = re.search(r"\[([A-Za-z0-9_.-]+)\]\s*:", block) if kind == "claim" else None
        out.append(
            {
                "file": str(path),
                "line": index + 1,
                "kind": kind,
                "claim_label": label_match.group(1) if label_match else "",
                "flags": ",".join(flags),
                "attributes": " | ".join(attributes),
                "text": block,
            }
        )
    return out


def main() -> int:
    all_records = [record for path in ROOTS for record in records(path)]
    with OUTPUT.open("w", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=["file", "line", "kind", "claim_label", "flags", "attributes", "text"],
            dialect="excel-tab",
        )
        writer.writeheader()
        writer.writerows(all_records)

    kinds = Counter(record["kind"] for record in all_records)
    flags = Counter(
        flag
        for record in all_records
        for flag in str(record["flags"]).split(",")
        if flag
    )
    per_file = Counter(str(record["file"]) for record in all_records)
    print(f"files={len(ROOTS)}")
    print(f"records={len(all_records)}")
    print(f"kinds={dict(sorted(kinds.items()))}")
    print(f"flags={dict(sorted(flags.items()))}")
    for path in ROOTS:
        print(f"file_records[{path}]={per_file[str(path)]}")
    print(f"output={OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
