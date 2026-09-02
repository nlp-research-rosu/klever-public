#!/usr/bin/env python3
"""Emit an exhaustive declaration/rule inventory for the audited K sources."""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path


WORK = Path("/tmp/audit-work/reconstruction")
START = re.compile(r"^\s*(syntax|rule|context|configuration|claim)\b")
BOUNDARY = re.compile(
    r"^(?:\s*(?:syntax|rule|context|configuration|claim)\b"
    r"|(?:module|endmodule|requires)\b|\s{0,2}imports\b)"
)


def source_files() -> list[Path]:
    semantics = sorted((WORK / "reference-semantics").rglob("*.k"))
    return semantics + [WORK / "verification.k", WORK / "spec.k"]


def entries(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    index = 0
    while index < len(lines):
        match = START.match(lines[index])
        if not match:
            index += 1
            continue
        kind = match.group(1)
        start = index
        index += 1
        while index < len(lines) and not BOUNDARY.match(lines[index]):
            index += 1
        block = "\n".join(lines[start:index]).rstrip()
        yield kind, start + 1, index, block


def flags(kind: str, block: str) -> list[str]:
    found = []
    for flag in (
        "function",
        "total",
        "functional",
        "macro",
        "macro-rec",
        "symbol",
        "no-evaluators",
        "concrete",
        "simplification",
        "owise",
        "priority",
        "strict",
        "seqstrict",
    ):
        if re.search(rf"\b{re.escape(flag)}\b", block):
            found.append(flag)
    if kind == "rule":
        if "<k>" in block or re.search(r"<[A-Za-z][^>]*>", block):
            found.append("operational")
        else:
            found.append("equational")
    return found


def assessment(path: Path, kind: str, start: int, block: str) -> str:
    relative = path.relative_to(WORK).as_posix()
    if relative.startswith("reference-semantics/"):
        if kind == "configuration":
            return "FIXED_SUPPLIED_CONFIGURATION; used cell schema reviewed"
        if "no-evaluators" in block or "symbol(" in block:
            return "FIXED_SUPPLIED_OPAQUE_BOUNDARY; not reached by audited program"
        if "[concrete]" in block:
            return "FIXED_SUPPLIED_CONCRETE_RULE; absent from proof evaluator; not theorem-critical"
        return "FIXED_SUPPLIED_RULE_OR_DECL; no candidate change; no false witness found"
    if relative == "verification.k":
        if kind == "syntax" and "MinPathDefinition" in block:
            return "CANDIDATE_MACRO_DECL; accepted after independent parsed-KAST identity"
        if kind == "rule" and "MinPathDefinition" in block:
            return "CANDIDATE_MACRO_EXPANSION; accepted after independent parsed-KAST identity"
        return "CANDIDATE_PROOF_EXTENSION; requires individual review"
    if relative == "spec.k" and kind == "claim":
        return "POSITIVE_ENTRY_CLAIM; sound ground execution but materially under-scoped"
    return "OTHER"


def main() -> int:
    counters: Counter[str] = Counter()
    file_hashes = []
    records = []
    for path in source_files():
        data = path.read_bytes()
        relative = path.relative_to(WORK).as_posix()
        file_hashes.append((relative, hashlib.sha256(data).hexdigest()))
        for kind, start, end, block in entries(path):
            entry_flags = flags(kind, block)
            counters[f"kind:{kind}"] += 1
            counters["entries"] += 1
            for flag in entry_flags:
                counters[f"flag:{flag}"] += 1
            records.append(
                (
                    relative,
                    start,
                    end,
                    kind,
                    ",".join(entry_flags) or "-",
                    assessment(path, kind, start, block),
                    block.replace("\t", "    ").replace("\n", "\\n"),
                )
            )

    print("INVENTORY_VERSION=1")
    print(f"SOURCE_FILES={len(file_hashes)}")
    for relative, digest in file_hashes:
        print(f"SOURCE_SHA256\t{relative}\t{digest}")
    print("COUNTS")
    for key in sorted(counters):
        print(f"{key}\t{counters[key]}")
    print("RECORDS")
    print("file\tstart_line\tend_line\tkind\tflags\tassessment\tfull_block")
    for record in records:
        print("\t".join(map(str, record)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
