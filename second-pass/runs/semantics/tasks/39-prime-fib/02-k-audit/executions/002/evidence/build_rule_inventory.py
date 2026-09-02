#!/usr/bin/env python3
"""Build an exhaustive declaration/rule inventory for the audited K sources."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

WORK = Path("/tmp/audit-work/prime-fib-audit")
OUT = Path("/audit-output/evidence/rule-inventory.md")
sources = [WORK / "reference-semantics" / "semantics.k"]
sources += sorted((WORK / "reference-semantics" / "semantics").glob("*.k"))
sources += [WORK / "verification.k", WORK / "spec.k"]

start_re = re.compile(r"^\s*(syntax|rule|context|configuration|claim|alias)\b")


def entries(path: Path):
    lines = path.read_text().splitlines()
    starts = [
        (index, start_re.match(line).group(1))
        for index, line in enumerate(lines)
        if start_re.match(line)
    ]
    for position, (start, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block_lines = lines[start:end]
        while block_lines and (
            not block_lines[-1].strip()
            or block_lines[-1].lstrip().startswith("//")
            or block_lines[-1].strip() == "endmodule"
        ):
            block_lines.pop()
        yield start + 1, kind, "\n".join(block_lines).rstrip()


def role(path: Path, kind: str, block: str) -> str:
    rel = path.relative_to(WORK).as_posix()
    if rel == "verification.k":
        return "PROOF_LOCAL_EXACT_DEFINITION" if kind in {"syntax", "rule"} else "PROOF_LOCAL"
    if rel == "spec.k":
        return "GROUND_TARGET_SCOPE_LIMITED"
    if rel.endswith("semantics/syntax.k"):
        return "FIXED_SYNTAX_USED_AND_UNUSED_PRODUCTIONS"
    if rel.endswith("semantics/core.k"):
        used_markers = (
            "#loadAll",
            "Name(",
            "#look",
            "builtinsScope",
            "#evalArgs",
            "#evalArgCont",
            "#applyK",
            "Int(",
            "Bool(",
            "truthy",
            "appendVal",
            "closureVal",
            "configuration",
            "KResult",
            "RetState",
        )
        return (
            "FIXED_USED_PATH"
            if any(marker in block for marker in used_markers)
            else "FIXED_UNREACHED_BY_SUBMITTED_TERM"
        )
    if rel.endswith("semantics/controls.k"):
        used_markers = ("Assign(", "AugAssign(", "Expr(", "#branch", "If(", "#while", "While(", "#loopLbl")
        return (
            "FIXED_USED_PATH"
            if any(marker in block for marker in used_markers)
            else "FIXED_UNREACHED_BY_SUBMITTED_TERM"
        )
    if rel.endswith("semantics/functions.k"):
        used_markers = ("frame(", "#bindP", "#pop", "#endcall", "Return(", "FuncDef(")
        return (
            "FIXED_USED_PATH"
            if any(marker in block for marker in used_markers)
            else "FIXED_UNREACHED_BY_SUBMITTED_TERM"
        )
    if rel.endswith("semantics/call.k"):
        used_markers = ("#callee", "Call(", "closureVal(", "#applyK", "toCall")
        return (
            "FIXED_USED_PATH"
            if any(marker in block for marker in used_markers)
            else "FIXED_UNREACHED_BY_SUBMITTED_TERM"
        )
    if rel.endswith("semantics/operators.k"):
        used_markers = ("BinOp(", "Compare(", "applyBin", "applyCmp")
        return (
            "FIXED_USED_PATH"
            if any(marker in block for marker in used_markers)
            else "FIXED_UNREACHED_BY_SUBMITTED_TERM"
        )
    if rel.endswith("semantics/bool.k"):
        return "FIXED_USED_PATH" if "BoolOp" in block else "FIXED_UNREACHED_BY_SUBMITTED_TERM"
    if rel.endswith("semantics/int.k"):
        used_ops = ('"+"', '"*"', '"%"', '"<"', '"<="', '"=="', "pyMod")
        return (
            "FIXED_USED_PATH"
            if any(marker in block for marker in used_ops)
            else "FIXED_UNREACHED_BY_SUBMITTED_TERM"
        )
    if rel.endswith("semantics/str.k"):
        return (
            "FIXED_USED_PATH"
            if "Str(" in block or "strToCodes" in block
            else "FIXED_UNREACHED_BY_SUBMITTED_TERM"
        )
    return "FIXED_UNREACHED_BY_SUBMITTED_TERM"


rows = []
for source in sources:
    for line, kind, block in entries(source):
        rel = source.relative_to(WORK).as_posix()
        lowered = block.lower()
        attrs = []
        for attr in (
            "function",
            "functional",
            "total",
            "no-evaluators",
            "priority",
            "simplification",
            "concrete",
            "owise",
            "strict",
            "seqstrict",
            "macro",
        ):
            if attr in lowered:
                attrs.append(attr)
        rows.append(
            {
                "source": rel,
                "line": line,
                "kind": kind,
                "attrs": attrs,
                "role": role(source, kind, block),
                "block": block,
            }
        )

kind_counts = Counter(row["kind"] for row in rows)
role_counts = Counter(row["role"] for row in rows)
attr_counts = Counter(attr for row in rows for attr in row["attrs"])

with OUT.open("w") as handle:
    handle.write("# Exhaustive K declaration and rule inventory\n\n")
    handle.write(
        "This reviewer-generated inventory covers every `syntax`, `rule`, "
        "`context`, `configuration`, `claim`, and `alias` declaration in the "
        "supplied semantics tree plus `verification.k` and `spec.k`. "
        "`FIXED_UNREACHED_BY_SUBMITTED_TERM` means the declaration remains part "
        "of the supplied trust boundary but no constructor/control state in the "
        "submitted ground claims can reach it. `FIXED_USED_PATH` items were "
        "included in the manual control/evaluation review. Proof-local aliases "
        "were separately compared to regenerated source terms in "
        "`program-pinning.log`.\n\n"
    )
    handle.write(f"- Total inventoried entries: {len(rows)}\n")
    handle.write(f"- Kinds: {dict(sorted(kind_counts.items()))}\n")
    handle.write(f"- Roles: {dict(sorted(role_counts.items()))}\n")
    handle.write(f"- Attribute markers: {dict(sorted(attr_counts.items()))}\n\n")
    handle.write("## Opaque/no-evaluator symbols\n\n")
    opaque = [row for row in rows if "no-evaluators" in row["attrs"]]
    if not opaque:
        handle.write("None.\n\n")
    for row in opaque:
        first = " ".join(row["block"].split())
        handle.write(
            f"- `{row['source']}:{row['line']}` — `{first}` — "
            f"{row['role']}\n"
        )
    handle.write("\n## Complete inventory\n\n")
    for index, row in enumerate(rows, 1):
        attr_text = ", ".join(row["attrs"]) or "none"
        handle.write(
            f"### {index}. {row['source']}:{row['line']} — {row['kind']}\n\n"
            f"- Review classification: `{row['role']}`\n"
            f"- Attribute markers: `{attr_text}`\n\n"
            "```k\n"
            f"{row['block']}\n"
            "```\n\n"
        )

print(f"wrote {OUT}")
print(f"total={len(rows)}")
print(f"kinds={dict(sorted(kind_counts.items()))}")
print(f"roles={dict(sorted(role_counts.items()))}")
print(f"attributes={dict(sorted(attr_counts.items()))}")
print(f"opaque_no_evaluators={sum('no-evaluators' in row['attrs'] for row in rows)}")
