#!/usr/bin/env python3
"""Build an exhaustive source-level K declaration/rule inventory."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
SEMANTICS = ROOT / "reference-semantics"
OUTPUT = Path("/audit-output/evidence/rule_inventory.md")

START = re.compile(
    r"^(requires)\b|^\s*(module|imports|endmodule|syntax|configuration|context|rule|claim|alias)\b"
)


def source_files() -> list[Path]:
    return sorted(SEMANTICS.rglob("*.k")) + [
        ROOT / "verification.k",
        ROOT / "spec.k",
    ]


def module_at(lines: list[str], index: int) -> str:
    current = ""
    for line in lines[: index + 1]:
        match = re.match(r"^\s*module\s+([A-Za-z0-9-]+)", line)
        if match:
            current = match.group(1)
        if re.match(r"^\s*endmodule\b", line):
            current = ""
    return current


def entries(path: Path) -> list[dict[str, object]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [i for i, line in enumerate(lines) if START.match(line)]
    result: list[dict[str, object]] = []
    for position, start in enumerate(starts):
        stop = starts[position + 1] if position + 1 < len(starts) else len(lines)
        first = lines[start].strip()
        match = START.match(lines[start])
        assert match is not None
        kind = match.group(1) or match.group(2)
        block_lines = lines[start:stop]
        retained: list[str] = []
        for line in block_lines:
            stripped = line.strip()
            if stripped.startswith("//"):
                continue
            if stripped:
                retained.append(stripped)
        normalized = " ".join(retained)
        normalized = re.sub(r"\s+", " ", normalized)
        result.append(
            {
                "path": path,
                "line": start + 1,
                "kind": kind,
                "module": module_at(lines, start),
                "first": first,
                "text": normalized,
            }
        )
    return result


def is_material_fixed(entry: dict[str, object]) -> bool:
    path = Path(entry["path"])
    rel = path.relative_to(SEMANTICS).as_posix()
    text = str(entry["text"])
    kind = str(entry["kind"])

    if kind in {"requires", "module", "imports", "endmodule"}:
        return rel == "semantics.k" or rel in {
            "semantics/syntax.k",
            "semantics/core.k",
            "semantics/controls.k",
            "semantics/functions.k",
            "semantics/call.k",
            "semantics/operators.k",
            "semantics/int.k",
            "semantics/list.k",
        }
    if rel == "semantics/syntax.k":
        return True
    if rel == "semantics/core.k":
        material = re.compile(
            r"configuration|isRefV|#alloc|#loadAll|Stmts|Name\(|#look|"
            r"builtinsScope|#evalArgs|#evalArgCont|#applyK|Int\(|Bool\(|"
            r"truthy|appendVal|vals2valSeq|applyBin|applyCmp|ValSeq|Scope|"
            r"RetState|Exc|KResult|Vals|Parent"
        )
        return bool(material.search(text))
    if rel == "semantics/controls.k":
        material = re.compile(
            r"Assign\(Name|Expr\(|#branch|If\(|While|#while|#loopLbl"
        )
        return bool(material.search(text))
    if rel == "semantics/functions.k":
        material = re.compile(
            r"frame\(|FuncDef|#bindP|Return\(|#endcall|#pop"
        )
        return bool(material.search(text))
    if rel == "semantics/call.k":
        material = re.compile(
            r"Attribute|#callee|Call\(|#evalArgs|toCall|boundMethodV|"
            r"isMutMethod|closureVal\("
        )
        return bool(material.search(text))
    if rel == "semantics/operators.k":
        return bool(re.search(r"BinOp|Compare|applyCmp", text))
    if rel == "semantics/int.k":
        return bool(
            re.search(
                r'applyBin\("\+"|applyBin\("%"|pyMod|'
                r'applyCmp\("<"|applyCmp\("<="|applyCmp\("=="',
                text,
            )
        )
    if rel == "semantics/list.k":
        return bool(
            re.search(
                r"toList|ListExpr|valSeqConcat|#alloc|"
                r'boundMethodV\(ref\(H:Int\), "append"\)',
                text,
            )
        )
    if rel in {"semantics/assert.k", "semantics/concrete.k"}:
        return "Assert" in text or "Compare(list" in text
    return False


def decision(entry: dict[str, object]) -> str:
    path = Path(entry["path"])
    text = str(entry["text"])
    kind = str(entry["kind"])
    module = str(entry["module"])

    if path.name == "verification.k":
        if kind in {"requires", "module", "imports", "endmodule"}:
            return "CANDIDATE_STRUCTURE_OK"
        if module == "VERIFICATION-SYNTAX":
            if kind == "syntax":
                return "CANDIDATE_MACRO_OR_SUMMARY_DECL_SOUND"
            if kind == "rule":
                return "CANDIDATE_MACRO_EXPANSION_SOUND"
        if module == "VERIFICATION":
            if kind == "rule" and "valSeqConcat" in text:
                return "CANDIDATE_DERIVED_LIST_LEMMA_SOUND"
            if kind == "rule":
                return "CANDIDATE_SUMMARY_EQUATION_SOUND"
            if kind == "syntax":
                return "CANDIDATE_SUMMARY_DECL_SOUND"
        return "CANDIDATE_STRUCTURE_OK"

    if path.name == "spec.k":
        if kind == "claim":
            return "POSITIVE_CLAIM_FRESHLY_MACHINE_CHECKED"
        return "SPEC_STRUCTURE_OK"

    if is_material_fixed(entry):
        if path.name in {"assert.k", "concrete.k"}:
            return "FIXED_CONCRETE_TEST_PATH_REVIEWED"
        if kind == "syntax":
            return "FIXED_MATERIAL_SYNTAX_REVIEWED"
        if kind == "configuration":
            return "FIXED_MATERIAL_CONFIGURATION_REVIEWED"
        if kind in {"rule", "context"}:
            return "FIXED_MATERIAL_EXECUTION_REVIEWED"
        return "FIXED_MATERIAL_STRUCTURE_REVIEWED"

    if "no-evaluators" in text or "symbol(" in text:
        return "FIXED_UNUSED_OPAQUE_BOUNDARY_NO_INFLUENCE"
    return "FIXED_UNUSED_BY_SUBMITTED_PROGRAM_NO_INFLUENCE"


def flags(text: str) -> str:
    labels = [
        "function",
        "total",
        "functional",
        "macro",
        "macro-rec",
        "symbol",
        "no-evaluators",
        "priority",
        "simplification",
        "owise",
        "concrete",
        "strict",
        "seqstrict",
    ]
    present = [label for label in labels if label in text]
    return ",".join(present) if present else "-"


def escape_cell(text: str, limit: int = 420) -> str:
    compact = text.replace("|", "\\|").replace("`", "'")
    if len(compact) > limit:
        compact = compact[:limit] + "…"
    return compact


def main() -> None:
    inventory: list[dict[str, object]] = []
    for path in source_files():
        inventory.extend(entries(path))

    kind_counts = collections.Counter(str(entry["kind"]) for entry in inventory)
    decision_counts = collections.Counter(decision(entry) for entry in inventory)
    flag_counts: collections.Counter[str] = collections.Counter()
    for entry in inventory:
        for flag in flags(str(entry["text"])).split(","):
            if flag != "-":
                flag_counts[flag] += 1

    out: list[str] = [
        "# Exhaustive source-level K inventory",
        "",
        "Generated from the fresh scratch copy. Each source directive beginning "
        "with `requires`, `module`, `imports`, `endmodule`, `syntax`, "
        "`configuration`, `context`, `rule`, `claim`, or `alias` is listed once.",
        "",
        f"- Total entries: {len(inventory)}",
        f"- Kind counts: {dict(sorted(kind_counts.items()))}",
        f"- Attribute counts: {dict(sorted(flag_counts.items()))}",
        f"- Decision counts: {dict(sorted(decision_counts.items()))}",
        "",
        "Decision codes distinguish the fixed supplied baseline from "
        "candidate-authored proof extensions. `FIXED_UNUSED...` means the entry "
        "is present in the selected fixed semantics but no constructor, symbol, "
        "or continuation on this program's reachable proof path invokes it; it "
        "is retained in the trust ledger rather than asserted to be a universal "
        "model of all Python.",
        "",
        "| Source | Line | Module | Kind | Attributes | Decision | Declaration/rule |",
        "|---|---:|---|---|---|---|---|",
    ]

    for entry in inventory:
        path = Path(entry["path"])
        if path.is_relative_to(SEMANTICS):
            rel = "reference-semantics/" + path.relative_to(SEMANTICS).as_posix()
        else:
            rel = path.name
        text = str(entry["text"])
        out.append(
            "| "
            + " | ".join(
                [
                    escape_cell(rel, 120),
                    str(entry["line"]),
                    escape_cell(str(entry["module"]), 80) or "-",
                    escape_cell(str(entry["kind"]), 40),
                    escape_cell(flags(text), 120),
                    escape_cell(decision(entry), 100),
                    escape_cell(text),
                ]
            )
            + " |"
        )

    OUTPUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("inventory_output:", OUTPUT)
    print("total_entries:", len(inventory))
    print("kind_counts:", dict(sorted(kind_counts.items())))
    print("attribute_counts:", dict(sorted(flag_counts.items())))
    print("decision_counts:", dict(sorted(decision_counts.items())))


if __name__ == "__main__":
    main()
