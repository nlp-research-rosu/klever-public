#!/usr/bin/env python3
"""Produce a complete, line-addressable inventory of K sentences in scope."""

from __future__ import annotations

import csv
import re
from pathlib import Path

TRUSTED_ROOT = Path("/reference/reference-semantics")
CANDIDATE_VERIFICATION = Path("/candidate/verification.k")
CANDIDATE_SPEC = Path("/candidate/spec.k")

START = re.compile(r"^  (syntax|rule|configuration|context|claim|alias)\b")
MODULE = re.compile(r"^module\s+(\S+)")
BOUNDARY = re.compile(
    r"^(?:module\b|endmodule\b|requires\b|  imports\b|  "
    r"(?:syntax|rule|configuration|context|claim|alias)\b)"
)


def decision(path: Path, line: int, kind: str, text: str) -> str:
    if path == CANDIDATE_VERIFICATION:
        if kind == "syntax" and line == 26:
            return (
                "EVIDENCE_GAP_OVERBROAD_TOTAL: equations cover empty rest for any Val "
                "and nonempty rest only for noneV/str; actual claims stay in covered cases"
            )
        if kind == "syntax":
            return "ACCEPT_LOCAL_DECLARATION: transparent proof-domain sort/function/macro"
        if kind == "rule" and line in (12, 13):
            return "ACCEPT_SOUND: structural string-only ValSeq embedding"
        if kind == "rule" and line in (18, 20):
            return (
                "ACCEPT_SOUND: exact composition of stringVals equation with fixed "
                "MPY-LIST iterator rule; continuation/cells preserved"
            )
        if kind == "rule" and line in (27, 28, 30, 33):
            return (
                "ACCEPT_SOUND_ON_MATCH_DOMAIN: terminating first-longest left fold; "
                "guards are disjoint/cover integer length comparison"
            )
        if kind == "rule" and line == 40:
            return "ACCEPT_SOUND: macro is byte-for-byte translated function closure body"
        return "REVIEWED_CANDIDATE_EXTENSION"
    if path == CANDIDATE_SPEC:
        return "TARGET_CLAIM: adequacy and reachability reviewed separately"
    return (
        "TRUSTED_FIXED_BASELINE: integrity-matched supplied semantics; "
        "not a candidate proof extension"
    )


def attrs(text: str) -> str:
    found: list[str] = []
    for name in (
        "function",
        "functional",
        "total",
        "simplification",
        "priority",
        "concrete",
        "macro",
        "macro-rec",
        "owise",
        "symbol",
        "no-evaluators",
        "strict",
        "seqstrict",
    ):
        if re.search(rf"\b{re.escape(name)}\b", text):
            found.append(name)
    return ",".join(found) if found else "-"


def records(path: Path) -> list[dict[str, object]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    module = "-"
    result: list[dict[str, object]] = []
    index = 0
    while index < len(lines):
        module_match = MODULE.match(lines[index])
        if module_match:
            module = module_match.group(1)
        start_match = START.match(lines[index])
        if not start_match:
            index += 1
            continue
        start = index
        kind = start_match.group(1)
        parts = [lines[index].strip()]
        index += 1
        while index < len(lines) and not BOUNDARY.match(lines[index]):
            stripped = lines[index].strip()
            if stripped and not stripped.startswith("//"):
                parts.append(stripped)
            index += 1
        text = " ".join(parts)
        result.append(
            {
                "source": str(path),
                "module": module,
                "line": start + 1,
                "kind": kind,
                "attributes": attrs(text),
                "decision": decision(path, start + 1, kind, text),
                "sentence": text,
            }
        )
    expected = sum(1 for line in lines if START.match(line))
    if expected != len(result):
        raise RuntimeError(f"{path}: expected {expected} records, made {len(result)}")
    return result


def main() -> int:
    paths = sorted(TRUSTED_ROOT.rglob("*.k"))
    paths.extend([CANDIDATE_VERIFICATION, CANDIDATE_SPEC])
    all_records = [record for path in paths for record in records(path)]
    writer = csv.DictWriter(
        __import__("sys").stdout,
        fieldnames=[
            "source",
            "module",
            "line",
            "kind",
            "attributes",
            "decision",
            "sentence",
        ],
        delimiter="\t",
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(all_records)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
