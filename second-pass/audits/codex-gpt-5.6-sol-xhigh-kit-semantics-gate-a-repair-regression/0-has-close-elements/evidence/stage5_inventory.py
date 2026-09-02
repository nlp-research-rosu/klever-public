#!/usr/bin/env python3
"""Produce a line-addressed inventory of every local K declaration and rule."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(
    r"^\s*(module|endmodule|imports|configuration|context|syntax|rule|claim)\b"
)
FILE_REQUIRE = re.compile(r'^requires\s+"')
TAGS = [
    "function",
    "total",
    "functional",
    "symbol",
    "no-evaluators",
    "priority",
    "owise",
    "concrete",
    "simplification",
    "macro-rec",
    "macro",
    "strict",
    "seqstrict",
]


def declarations(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = []
    in_block_comment = False
    for index, raw in enumerate(lines):
        probe = raw.split("//", 1)[0]
        if in_block_comment:
            if "*/" in probe:
                probe = probe.split("*/", 1)[1]
                in_block_comment = False
            else:
                continue
        while "/*" in probe:
            before, after = probe.split("/*", 1)
            if "*/" in after:
                after = after.split("*/", 1)[1]
                probe = before + after
            else:
                probe = before
                in_block_comment = True
                break
        match = START.match(probe)
        if match:
            starts.append((index, match.group(1)))
        elif FILE_REQUIRE.match(probe):
            starts.append((index, "requires"))

    for position, (start, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block = lines[start:end]
        while block and (not block[-1].strip() or block[-1].lstrip().startswith("//")):
            block.pop()
        yield start + 1, kind, "\n".join(block)


def tag_block(kind: str, text: str) -> list[str]:
    found = []
    lowered = text.lower()
    for tag in TAGS:
        if re.search(rf"(?<![a-z-]){re.escape(tag)}(?:\(|\b)", lowered):
            found.append(tag)
    if kind == "rule":
        if "<k>" in text:
            found.append("operational-rule")
        elif "macro" in found or "macro-rec" in found:
            found.append("macro-rule")
        else:
            found.append("equational-rule")
    return found


def relevance(path: Path, kind: str, text: str) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel in {"verification.k", "spec.k"}:
        return "CANDIDATE-PROOF-LOCAL"
    used_tokens = (
        "#loadAll",
        "Module(",
        "FuncDef(",
        "ImportFrom(",
        "Assign(Name",
        "AugAssign(Name",
        "While(",
        "#while",
        "#whileCond",
        "#loopLbl",
        "If(",
        "#branch",
        "Return(",
        "#pop",
        "#endcall",
        "#bindP",
        "Call(",
        "#callee",
        "#evalArgs",
        "#evalArgCont",
        "#applyK(toCall(closureVal",
        'builtinV("len")',
        'builtinV("abs")',
        'applyBuiltin("len"',
        'applyBuiltin("abs"',
        "seqLen(",
        "vsLen(",
        "Name(",
        "#look",
        "Int(",
        "Bool(",
        "Float(",
        "BinOp(",
        "Compare(",
        "applyBin(",
        "applyCmp(",
        "Subscript(",
        "applyIndex(",
        "valSeqAt(",
        "normIdx(",
        "floatLt(",
        "absF(",
        "subF(",
        "truthy(",
        "builtinsScope",
        "configuration",
    )
    if any(token in text for token in used_tokens):
        return "PROGRAM-PATH-OR-SHARED-DISPATCH"
    if kind in {"requires", "module", "endmodule", "imports", "syntax", "context"}:
        return "FIXED-BASELINE-DECLARATION"
    return "FIXED-BASELINE-UNUSED-BY-SUBMITTED-PROGRAM"


def main() -> None:
    counts = Counter()
    tag_counts = Counter()
    relevance_counts = Counter()
    records = []
    for path in FILES:
        for line, kind, text in declarations(path):
            tags = tag_block(kind, text)
            rel = relevance(path, kind, text)
            counts[kind] += 1
            tag_counts.update(tags)
            relevance_counts[rel] += 1
            records.append((path.relative_to(ROOT).as_posix(), line, kind, tags, rel, text))

    print("INVENTORY_SCOPE:")
    for path in FILES:
        print(f"  {path.relative_to(ROOT).as_posix()}")
    print(f"FILES={len(FILES)}")
    print(f"RECORDS={len(records)}")
    print("KIND_COUNTS=" + repr(dict(sorted(counts.items()))))
    print("TAG_COUNTS=" + repr(dict(sorted(tag_counts.items()))))
    print("RELEVANCE_COUNTS=" + repr(dict(sorted(relevance_counts.items()))))
    print()
    for ordinal, (path, line, kind, tags, rel, text) in enumerate(records, 1):
        one_line = " ".join(part.strip() for part in text.splitlines() if part.strip())
        print(
            f"{ordinal:04d}\t{path}:{line}\tKIND={kind}\t"
            f"TAGS={','.join(tags) if tags else '-'}\tRELEVANCE={rel}"
        )
        print(f"      {one_line}")


if __name__ == "__main__":
    main()
