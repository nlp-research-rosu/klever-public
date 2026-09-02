#!/usr/bin/env python3
"""Extract an exhaustive, line-addressable inventory of local K declarations."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


TRUSTED_ROOT = Path("/reference/reference-semantics")
CANDIDATE_VERIFICATION = Path("/candidate/verification.k")
OUTPUT = Path("/audit-output/evidence/rule-inventory.tsv")
SUMMARY = Path("/audit-output/evidence/rule-inventory-summary.txt")

START = re.compile(
    r'^\s*(?:(requires)\s+"|(module|imports|configuration|syntax|context|rule|claim|endmodule)\b)'
)
INVENTORY_KINDS = {
    "requires",
    "module",
    "imports",
    "configuration",
    "syntax",
    "context",
    "rule",
    "claim",
    "endmodule",
}
FLAGS = [
    "function",
    "functional",
    "total",
    "macro",
    "macro-rec",
    "symbol",
    "no-evaluators",
    "priority",
    "owise",
    "concrete",
    "simplification",
    "strict",
    "seqstrict",
]


def source_files() -> list[Path]:
    return sorted(TRUSTED_ROOT.rglob("*.k")) + [CANDIDATE_VERIFICATION]


def inventory_file(path: Path) -> list[dict[str, str | int]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            kind = match.group(1) or match.group(2)
            if kind in INVENTORY_KINDS:
                starts.append((index, kind))

    entries: list[dict[str, str | int]] = []
    for position, (start, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block_lines = lines[start:end]
        while block_lines and (
            not block_lines[-1].strip() or block_lines[-1].lstrip().startswith("//")
        ):
            block_lines.pop()
        text = "\n".join(block_lines)
        flags = ",".join(flag for flag in FLAGS if re.search(rf"\b{re.escape(flag)}\b", text))
        origin = "candidate-proof-extension" if path == CANDIDATE_VERIFICATION else "trusted-supplied"
        entries.append(
            {
                "origin": origin,
                "path": str(path),
                "start": start + 1,
                "end": start + len(block_lines),
                "kind": kind,
                "flags": flags or "-",
                "text": text.replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n"),
            }
        )
    return entries


def main() -> int:
    entries = [entry for path in source_files() for entry in inventory_file(path)]
    with OUTPUT.open("w", encoding="utf-8") as stream:
        stream.write("origin\tpath\tstart\tend\tkind\tflags\texact_source_block\n")
        for entry in entries:
            stream.write(
                "{origin}\t{path}\t{start}\t{end}\t{kind}\t{flags}\t{text}\n".format(
                    **entry
                )
            )

    by_kind = Counter(str(entry["kind"]) for entry in entries)
    by_origin_kind = Counter(
        (str(entry["origin"]), str(entry["kind"])) for entry in entries
    )
    with SUMMARY.open("w", encoding="utf-8") as stream:
        stream.write(f"source_files={len(source_files())}\n")
        stream.write(f"inventory_entries={len(entries)}\n")
        for kind, count in sorted(by_kind.items()):
            stream.write(f"kind.{kind}={count}\n")
        for (origin, kind), count in sorted(by_origin_kind.items()):
            stream.write(f"origin_kind.{origin}.{kind}={count}\n")
        for flag in FLAGS:
            count = sum(
                1
                for entry in entries
                if flag in str(entry["flags"]).split(",")
            )
            stream.write(f"flag.{flag}={count}\n")
        for path in source_files():
            count = sum(1 for entry in entries if entry["path"] == str(path))
            stream.write(f"file.{path}={count}\n")

    print(SUMMARY.read_text(encoding="utf-8"), end="")
    print(f"inventory_path={OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
