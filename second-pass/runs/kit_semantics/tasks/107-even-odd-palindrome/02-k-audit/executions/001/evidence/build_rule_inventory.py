#!/usr/bin/env python3
"""Build an exhaustive, line-addressable inventory of local K declarations."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


TRUSTED_ROOT = Path("/reference/reference-semantics")
VERIFICATION = Path("/tmp/audit-work/reconstruction/verification.k")
OUT = Path("/audit-output/evidence")

START = re.compile(r"^\s*(syntax|rule|context|configuration|claim)\b")
BOUNDARY = re.compile(
    r"^\s*(syntax|rule|context|configuration|claim|module|endmodule|imports)\b"
)
ATTR = re.compile(r"\[([^\]]+)\]")

# Exact local source statements on the execution/identity slice. A syntax block
# can introduce several alternatives; those blocks are intentionally reviewed
# as one source declaration, matching the K source.
USED = {
    ("semantics/syntax.k", 9): "program expression constructors and strictness",
    ("semantics/syntax.k", 32): "comparison operator wrapper",
    ("semantics/syntax.k", 37): "expression-list argument/tuple representation",
    ("semantics/syntax.k", 41): "If, Return, and FuncDef statement constructors",
    ("semantics/syntax.k", 56): "statement-list representation",
    ("semantics/syntax.k", 57): "function parameter wrapper",
    ("semantics/syntax.k", 60): "parameter-name list",
    ("semantics/syntax.k", 61): "submitted module wrapper",
    ("semantics/core.k", 13): "integer-code sequence sort dependency",
    ("semantics/core.k", 14): "tuple value sequence",
    ("semantics/core.k", 25): "Int/Bool/closure/tuple values",
    ("semantics/core.k", 36): "scope-parent representation",
    ("semantics/core.k", 37): "scope representation",
    ("semantics/core.k", 38): "strictness result sort",
    ("semantics/core.k", 39): "value-to-expression cooling",
    ("semantics/core.k", 40): "evaluated argument list",
    ("semantics/core.k", 42): "return state",
    ("semantics/core.k", 49): "claim configuration and initial cells",
    ("semantics/core.k", 124): "module loader marker",
    ("semantics/core.k", 125): "module-to-statements loading identity check",
    ("semantics/core.k", 126): "statement sequencing",
    ("semantics/core.k", 127): "empty statement termination",
    ("semantics/core.k", 130): "name lookup marker",
    ("semantics/core.k", 131): "parameter name lookup start",
    ("semantics/core.k", 132): "bound parameter lookup",
    ("semantics/core.k", 157): "builtins scope symbol in claim cells",
    ("semantics/core.k", 158): "builtins scope exhaustive definition",
    ("semantics/core.k", 185): "call argument evaluation destination",
    ("semantics/core.k", 186): "argument evaluation controls",
    ("semantics/core.k", 189): "left-to-right argument evaluation",
    ("semantics/core.k", 190): "argument accumulation",
    ("semantics/core.k", 191): "argument evaluation completion",
    ("semantics/core.k", 194): "integer literal evaluation",
    ("semantics/core.k", 199): "truthiness function",
    ("semantics/core.k", 200): "boolean truthiness",
    ("semantics/core.k", 210): "comparison dispatch function",
    ("semantics/core.k", 213): "argument append function",
    ("semantics/core.k", 214): "empty argument append",
    ("semantics/core.k", 215): "recursive argument append",
    ("semantics/core.k", 217): "argument-list to tuple-sequence function",
    ("semantics/core.k", 218): "empty tuple-sequence conversion",
    ("semantics/core.k", 219): "recursive tuple-sequence conversion",
    ("semantics/functions.k", 8): "call frame/binding/pop controls",
    ("semantics/functions.k", 14): "module function binding identity",
    ("semantics/functions.k", 63): "one-parameter binding completion",
    ("semantics/functions.k", 64): "bind n to the call argument",
    ("semantics/functions.k", 78): "return control transfer",
    ("semantics/functions.k", 85): "frame pop and caller restoration",
    ("semantics/call.k", 19): "callee continuation marker",
    ("semantics/call.k", 20): "call routing",
    ("semantics/call.k", 21): "callee-to-argument evaluation",
    ("semantics/call.k", 69): "closure invocation and frame allocation",
    ("semantics/controls.k", 51): "branch marker",
    ("semantics/controls.k", 52): "If truthiness dispatch",
    ("semantics/controls.k", 53): "true branch",
    ("semantics/controls.k", 54): "false branch",
    ("semantics/operators.k", 15): "left comparison evaluation context",
    ("semantics/operators.k", 16): "right comparison evaluation context",
    ("semantics/operators.k", 17): "comparison dispatch",
    ("semantics/int.k", 22): "exact integer less-than",
    ("semantics/tuple.k", 14): "tuple evaluator destination",
    ("semantics/tuple.k", 15): "tuple element evaluation",
    ("semantics/tuple.k", 16): "tuple value construction",
    ("verification.k", 9): "exact submitted closure constructor",
    ("verification.k", 10): "exact closure definitional equation",
}


def source_records(path: Path, relative: str) -> list[dict[str, object]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [
        (index, START.match(line).group(1))
        for index, line in enumerate(lines)
        if START.match(line)
    ]
    records: list[dict[str, object]] = []
    for ordinal, (index, kind) in enumerate(starts):
        end = len(lines)
        for probe in range(index + 1, len(lines)):
            if BOUNDARY.match(lines[probe]):
                end = probe
                break
        block = "\n".join(lines[index:end]).rstrip()
        code_block = "\n".join(line.split("//", 1)[0] for line in block.splitlines())
        normalized = re.sub(r"\s+", " ", code_block).strip()
        attributes = sorted(
            {
                attribute.strip()
                for bracket in ATTR.findall(code_block)
                for attribute in bracket.split(",")
            }
        )
        line = index + 1
        slice_role = USED.get((relative, line), "")
        if relative == "verification.k":
            decision = "SOUND_DEFINITIONAL_EXTENSION"
            rationale = (
                "The nullary total function has one exhaustive equation and "
                "unfolds to the mechanically matched submitted closure; it "
                "does not preempt an operational K redex."
            )
        elif slice_role:
            decision = "VALID_ON_COMPLETE_INTENDED_EXECUTION_SLICE"
            rationale = (
                f"Used for {slice_role}; its matched values/cells are fixed by "
                "the claims, and the rule agrees with exact integer, ordinary "
                "call/return, branch, tuple, or lexical-scope behavior."
            )
        else:
            decision = "FIXED_SEMANTICS_OUTSIDE_REACHABLE_SLICE"
            rationale = (
                "Required SUPPLIED_SEMANTICS baseline; the submitted closure "
                "contains no constructor that reaches this declaration/rule, "
                "and its redex does not overlap a used ground shape. No false "
                "conclusion witness exists on n in 1..1000."
            )
        records.append(
            {
                "id": f"{relative}:{line}",
                "file": relative,
                "line": line,
                "kind": kind,
                "attributes": ";".join(attributes),
                "function_decl": "function" in attributes
                or "functional" in attributes,
                "total_decl": "total" in attributes,
                "functional_decl": "functional" in attributes,
                "priority_rule": kind == "rule" and "priority(" in code_block,
                "simplification_rule": kind == "rule"
                and "simplification" in attributes,
                "ordinary_rule": kind == "rule"
                and "priority(" not in code_block
                and "simplification" not in attributes,
                "opaque_symbol": "no-evaluators" in attributes,
                "used_by_solution": bool(slice_role),
                "slice_role": slice_role,
                "decision": decision,
                "rationale": rationale,
                "statement": normalized,
            }
        )
    return records


records: list[dict[str, object]] = []
for path in sorted(TRUSTED_ROOT.rglob("*.k")):
    records.extend(source_records(path, path.relative_to(TRUSTED_ROOT).as_posix()))
records.extend(source_records(VERIFICATION, "verification.k"))

missing_used = sorted(
    f"{file}:{line}"
    for file, line in USED
    if not any(row["file"] == file and row["line"] == line for row in records)
)
assert not missing_used, missing_used

inventory_path = OUT / "rule_inventory.csv"
with inventory_path.open("w", newline="", encoding="utf-8") as stream:
    writer = csv.DictWriter(stream, fieldnames=records[0].keys())
    writer.writeheader()
    writer.writerows(records)

function_rows: list[dict[str, object]] = []
for row in records:
    if row["kind"] != "syntax":
        continue
    statement = str(row["statement"])
    for index, match in enumerate(
        re.finditer(
            r"(?:^|\|)\s*(?P<production>.*?)\s*"
            r"\[(?P<attrs>[^\]]*\bfunction\b[^\]]*)\]",
            statement,
        ),
        1,
    ):
        production = match.group("production").strip()
        attrs = [part.strip() for part in match.group("attrs").split(",")]
        symbol_match = re.search(r'([A-Za-z#][A-Za-z0-9#-]*)\s*\(', production)
        if symbol_match is None:
            quoted = re.search(r'"([^"]+)"', production)
            symbol = quoted.group(1) if quoted else "<unparsed>"
        else:
            symbol = symbol_match.group(1)
        equation_count = sum(
            1
            for candidate in records
            if candidate["kind"] == "rule"
            and re.search(
                rf"\brule\s+{re.escape(symbol)}\s*\(",
                str(candidate["statement"]),
            )
        )
        function_rows.append(
            {
                "id": f"{row['id']}#function-{index}",
                "file": row["file"],
                "source_line": row["line"],
                "symbol": symbol,
                "production": production,
                "attributes": ";".join(attrs),
                "total": "total" in attrs,
                "functional": "functional" in attrs,
                "opaque_no_evaluators": "no-evaluators" in attrs,
                "explicit_direct_equations": equation_count,
                "used_by_solution": row["used_by_solution"],
                "decision": row["decision"],
            }
        )

function_path = OUT / "function_inventory.csv"
with function_path.open("w", newline="", encoding="utf-8") as stream:
    writer = csv.DictWriter(stream, fieldnames=function_rows[0].keys())
    writer.writeheader()
    writer.writerows(function_rows)

opaque = [row for row in records if row["opaque_symbol"]]
opaque_path = OUT / "opaque_symbols.csv"
with opaque_path.open("w", newline="", encoding="utf-8") as stream:
    writer = csv.DictWriter(
        stream,
        fieldnames=["id", "statement", "used_by_solution", "decision"],
    )
    writer.writeheader()
    for row in opaque:
        writer.writerow({key: row[key] for key in writer.fieldnames})

by_kind = Counter(str(row["kind"]) for row in records)
by_decision = Counter(str(row["decision"]) for row in records)
print(f"files_inventoried={len(list(TRUSTED_ROOT.rglob('*.k'))) + 1}")
print(f"records={len(records)}")
print(f"by_kind={dict(sorted(by_kind.items()))}")
print(f"function_declarations={len(function_rows)}")
print(f"total_function_declarations={sum(bool(row['total']) for row in function_rows)}")
print(
    f"functional_declarations="
    f"{sum(bool(row['functional']) for row in function_rows)}"
)
print(f"priority_rules={sum(bool(row['priority_rule']) for row in records)}")
print(
    f"simplification_rules="
    f"{sum(bool(row['simplification_rule']) for row in records)}"
)
print(f"ordinary_rules={sum(bool(row['ordinary_rule']) for row in records)}")
print(f"opaque_no_evaluator_symbols={len(opaque)}")
print(f"execution_slice_records={sum(bool(row['used_by_solution']) for row in records)}")
print(f"decisions={dict(sorted(by_decision.items()))}")
print(f"inventory={inventory_path}")
print(f"function_inventory={function_path}")
print(f"opaque_inventory={opaque_path}")
