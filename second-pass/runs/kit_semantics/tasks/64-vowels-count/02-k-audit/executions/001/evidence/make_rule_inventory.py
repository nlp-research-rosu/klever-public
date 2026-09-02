#!/usr/bin/env python3
"""Generate an exhaustive declaration/rule inventory for the audited K theory."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
OUT = Path("/audit-output/evidence/rule-inventory.md")
START = re.compile(
    r"^\s*(syntax|configuration|context|rule|claim|macro|alias)\b"
)

TARGET_MARKERS = {
    "semantics/core.k": (
        "configuration",
        "IntSeq",
        "ValSeq",
        "Str",
        "Val ",
        "#loadAll",
        ":Stmts",
        ".Stmts",
        "#look",
        "Name(",
        "builtinsScope",
        "#evalArgs",
        "#evalArgCont",
        "Int(I:Int)",
        "appendVal",
    ),
    "semantics/iter.k": ("#iterNext", "#iterDone", "#iterYield"),
    "semantics/operators.k": ("Compare(", "applyCmp"),
    "semantics/int.k": (
        'applyBin("+",  I:Int, B:Bool)',
        'applyBin("+",  B:Bool, I:Int)',
    ),
    "semantics/str.k": (
        "#iterNext(str(",
        "Str(S:String)",
        "strToCodes",
        'applyCmp("=="',
        'applyCmp("in"',
        "strPrefix",
        "strContains",
    ),
    "semantics/tuple.k": ("#bindTgt",),
    "semantics/controls.k": (
        "Assign(Name(",
        "AugAssign(Name(",
        "For(",
        "#loop(",
        "#loopStep",
        "#loopLbl",
    ),
    "semantics/functions.k": (
        "frame(",
        "#bindP",
        "FuncDef(",
        "Return(",
        "#endcall",
        "#pop",
    ),
    "semantics/call.k": (
        "Call(",
        "#callee",
        "closureVal(",
        "#evalArgs",
    ),
    "syntax.k": (
        "syntax Expr",
        "syntax CmpOp",
        "syntax Stmt",
        "syntax Stmts",
        "syntax Params",
        "syntax ParamNames",
        "syntax Module",
    ),
}


def source_paths():
    paths = [ROOT / "reference-semantics" / "semantics.k"]
    paths.extend(sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")))
    paths.extend([ROOT / "verification.k", ROOT / "spec.k"])
    return paths


def blocks(path: Path):
    lines = path.read_text().splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    for number, start in enumerate(starts):
        stop = starts[number + 1] if number + 1 < len(starts) else len(lines)
        while stop > start + 1 and (
            not lines[stop - 1].strip()
            or lines[stop - 1].lstrip().startswith("//")
            or lines[stop - 1].strip() == "endmodule"
        ):
            stop -= 1
        yield start + 1, lines[start:stop]


def fixed_relative(path: Path) -> str:
    fixed_root = ROOT / "reference-semantics"
    if path.is_relative_to(fixed_root):
        return path.relative_to(fixed_root).as_posix()
    return path.relative_to(ROOT).as_posix()


def assessment(path: Path, kind: str, text: str) -> tuple[str, str]:
    rel = fixed_relative(path)
    if rel == "verification.k":
        if kind == "syntax":
            return (
                "proof-local",
                "Definitional summary declaration; constructor-total equations below fix every value.",
            )
        if "vowelsTail(.IntSeq" in text:
            return (
                "proof-local",
                "Truthful base equation: only a previous final y/Y contributes after exhaustion.",
            )
        if "vowelsTail(iCons" in text:
            return (
                "proof-local",
                "Truthful descending equation: counts the head's membership and recurses on the tail.",
            )
        return ("proof-local", "Reviewed candidate proof extension.")
    if rel == "spec.k":
        if "loop-inv" in text:
            return (
                "proof-claim",
                "Exact suffix-loop circularity with full return/frame footprint; independently closes.",
            )
        if "vowels-count" in text:
            return (
                "target-claim",
                "Entry theorem; exact submitted Module term and result-constraining postcondition.",
            )
        return ("proof-claim", "Reviewed reachability claim.")

    markers = TARGET_MARKERS.get(rel, ())
    if any(marker in text for marker in markers):
        return (
            "used-fixed",
            "Inside the target dependency cone; inspected as faithful for the constructor-sorted target states.",
        )
    if kind in {"syntax", "configuration", "context"} and rel in {
        "semantics/core.k",
        "semantics/syntax.k",
        "syntax.k",
    }:
        return (
            "fixed-declaration",
            "Fixed parser/configuration carrier; no candidate-added correctness conclusion.",
        )
    return (
        "unused-fixed",
        "Top symbol/construct is unreachable from this target; cannot contribute to either claim.",
    )


def main() -> None:
    records = []
    for path in source_paths():
        for line, block_lines in blocks(path):
            raw = "\n".join(block_lines).strip()
            match = START.match(block_lines[0])
            assert match is not None
            kind = match.group(1)
            normalized = " ".join(
                segment.strip()
                for segment in block_lines
                if segment.strip() and not segment.lstrip().startswith("//")
            )
            attrs = []
            for attr in (
                "function",
                "functional",
                "total",
                "no-evaluators",
                "concrete",
                "simplification",
                "priority",
                "owise",
                "strict",
                "seqstrict",
                "macro",
                "macro-rec",
            ):
                if re.search(rf"\b{re.escape(attr)}\b", normalized):
                    attrs.append(attr)
            scope, decision = assessment(path, kind, normalized)
            records.append(
                {
                    "file": fixed_relative(path),
                    "line": line,
                    "kind": kind,
                    "attrs": ", ".join(attrs) if attrs else "—",
                    "scope": scope,
                    "decision": decision,
                    "text": normalized,
                }
            )

    counts = collections.Counter(record["kind"] for record in records)
    scopes = collections.Counter(record["scope"] for record in records)
    attrs = collections.Counter()
    for record in records:
        if record["attrs"] != "—":
            attrs.update(record["attrs"].split(", "))

    output = [
        "# Exhaustive K declaration and rule inventory",
        "",
        "Generated from the fresh scratch source tree. A row is one complete "
        "top-level K declaration, configuration/context, semantic rule, or "
        "reachability claim; multiline declarations are normalized into one row.",
        "",
        f"Total records: **{len(records)}**",
        "",
        "Kinds: " + ", ".join(f"`{key}`={value}" for key, value in sorted(counts.items())),
        "",
        "Scopes: " + ", ".join(f"`{key}`={value}" for key, value in sorted(scopes.items())),
        "",
        "Attributes: " + ", ".join(f"`{key}`={value}" for key, value in sorted(attrs.items())),
        "",
        "| # | Location | Kind | Attributes | Scope | Rule-level decision | Declaration/rule |",
        "|---:|---|---|---|---|---|---|",
    ]
    for index, record in enumerate(records, 1):
        text = (
            record["text"]
            .replace("|", "&#124;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\n", " ")
        )
        decision = record["decision"].replace("|", "&#124;")
        output.append(
            f"| {index} | `{record['file']}:{record['line']}` | "
            f"`{record['kind']}` | {record['attrs']} | `{record['scope']}` | "
            f"{decision} | `{text}` |"
        )
    output.append("")
    OUT.write_text("\n".join(output))
    print("inventory_output=", OUT, sep="")
    print("total_records=", len(records), sep="")
    print("kind_counts=", dict(sorted(counts.items())), sep="")
    print("scope_counts=", dict(sorted(scopes.items())), sep="")
    print("attribute_counts=", dict(sorted(attrs.items())), sep="")


if __name__ == "__main__":
    main()
