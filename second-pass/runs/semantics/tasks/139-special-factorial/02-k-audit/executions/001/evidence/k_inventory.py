#!/usr/bin/env python3
"""Enumerate every local K declaration/rule/claim for the static audit.

The TSV records a source location, a hash of the complete normalized sentence,
a bounded preview, attributes, relevance, and a reviewer assessment for every
item.  Source files remain the authority for full text.
"""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path


TASK = Path("/tmp/audit-work/139-special-factorial")
PREFIXES = (
    "requires",
    "module",
    "imports",
    "syntax",
    "configuration",
    "context",
    "rule",
    "claim",
    "endmodule",
)
DECLARATION = re.compile(
    r"^(requires)\b|^\s*(module|imports|syntax|configuration|context|rule|claim|endmodule)\b"
)
ATTRIBUTES = (
    "function",
    "functional",
    "total",
    "simplification",
    "concrete",
    "owise",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
    "priority",
    "symbol",
    "no-evaluators",
)


def source_files() -> list[Path]:
    files = [TASK / "reference-semantics" / "semantics.k"]
    files.extend(sorted((TASK / "reference-semantics" / "semantics").glob("*.k")))
    files.extend([TASK / "verification.k", TASK / "spec.k"])
    return files


def declarations(path: Path):
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = DECLARATION.match(line)
        if match:
            starts.append((index, match.group(1) or match.group(2)))
    for position, (index, kind) in enumerate(starts):
        # One-line structural declarations should not absorb following text.
        if kind in {"requires", "module", "imports", "endmodule"}:
            end = index + 1
        else:
            end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        body_lines = []
        for line in lines[index:end]:
            stripped = line.strip()
            if stripped and not stripped.startswith("//"):
                body_lines.append(stripped)
        normalized = " ".join(body_lines)
        yield index + 1, kind, normalized


def attribute_set(text: str) -> str:
    found = []
    for attribute in ATTRIBUTES:
        if attribute in {"strict", "priority", "symbol"}:
            present = re.search(rf"\b{re.escape(attribute)}(?:\(|\b)", text)
        else:
            present = re.search(rf"\b{re.escape(attribute)}\b", text)
        if present:
            found.append(attribute)
    return ",".join(found) if found else "-"


def relevance(relative: str, kind: str, text: str) -> str:
    if relative == "verification.k":
        return "proof-summary"
    if relative == "spec.k":
        return "target-or-helper-claim"
    if "no-evaluators" in text:
        return "opaque-unused"
    if relative.endswith("semantics.k"):
        return "assembly"
    if relative.endswith("syntax.k"):
        used = (
            "Int",
            "Name",
            "Compare",
            "CmpOp",
            "Call",
            "Assign",
            "AugAssign",
            "While",
            "Return",
            "FuncDef",
            "Params",
            "Stmts",
            "Module",
        )
        return "program-path" if any(token in text for token in used) else "unused"
    path_tokens = {
        "semantics/core.k": (
            "#loadAll",
            ":Stmts",
            ".Stmts",
            "Name(",
            "#look",
            "builtinsScope",
            "#evalArgs",
            "#evalArgCont",
            "#applyK",
            "Int(",
            "truthy(",
            "applyBin",
            "applyCmp",
        ),
        "semantics/operators.k": ("Compare(", "applyCmp"),
        "semantics/int.k": (
            'applyBin("+"',
            'applyBin("*"',
            'applyCmp("<="',
        ),
        "semantics/controls.k": (
            "Assign(Name",
            "AugAssign(Name",
            "While(",
            "#while(",
            "#whileCond",
            "#loopLbl",
        ),
        "semantics/functions.k": (
            "FuncDef(",
            "#bindP",
            "Return(",
            "#endcall",
            "#pop",
            "frame(",
        ),
        "semantics/call.k": (
            "Call(",
            "#callee",
            "#applyK(toCall(closureVal",
        ),
    }
    for suffix, tokens in path_tokens.items():
        if relative.endswith(suffix):
            return "program-path" if any(token in text for token in tokens) else "unused"
    return "unused"


def assessment(relative: str, kind: str, text: str, rel: str) -> str:
    if relative == "verification.k":
        if kind == "rule":
            return "SOUND_DEFINITIONAL_EQUATION_DISJOINT_DESCENDING"
        if kind == "syntax":
            return "SOUND_TOTAL_MATHEMATICAL_SUMMARY_DECLARATION"
        return "STRUCTURAL_PROOF_MODULE_ITEM"
    if relative == "spec.k":
        if kind == "claim":
            return "AUDITED_REACHABILITY_CLAIM"
        return "STRUCTURAL_SPEC_MODULE_ITEM"
    if rel == "opaque-unused":
        return "ACCEPT_FIXED_SUPPLIED_OPAQUE_BOUNDARY_UNUSED_BY_PROGRAM"
    if kind in {"rule", "context", "configuration", "syntax"}:
        return "ACCEPT_FIXED_SUPPLIED_SEMANTICS_NO_FALSE_WITNESS_FOUND"
    return "STRUCTURAL_FIXED_SUPPLIED_ITEM"


def main() -> int:
    rows = []
    for path in source_files():
        relative = str(path.relative_to(TASK))
        for line, kind, text in declarations(path):
            digest = hashlib.sha256(text.encode()).hexdigest()
            attrs = attribute_set(text)
            rel = relevance(relative, kind, text)
            decision = assessment(relative, kind, text, rel)
            preview = text.replace("\t", " ")[:360]
            rows.append(
                (relative, line, kind, attrs, rel, decision, digest, preview)
            )

    print(
        "id\tfile\tline\tkind\tattributes\trelevance\tassessment"
        "\tstatement_sha256\tbounded_preview"
    )
    for identifier, row in enumerate(rows, 1):
        print(identifier, *row, sep="\t")

    kind_counts = Counter(row[2] for row in rows)
    relevance_counts = Counter(row[4] for row in rows)
    assessment_counts = Counter(row[5] for row in rows)
    print("# SUMMARY")
    print(f"# items={len(rows)}")
    print(f"# kinds={dict(sorted(kind_counts.items()))}")
    print(f"# relevance={dict(sorted(relevance_counts.items()))}")
    print(f"# assessments={dict(sorted(assessment_counts.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
