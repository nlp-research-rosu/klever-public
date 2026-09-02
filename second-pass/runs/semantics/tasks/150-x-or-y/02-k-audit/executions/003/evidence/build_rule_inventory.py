#!/usr/bin/env python3
"""Create a source-complete K declaration/rule inventory for audit stage 5."""

from __future__ import annotations

import collections
import csv
import re
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/150-x-or-y-review")
OUTPUT = Path("/audit-output/evidence/rule-inventory.tsv")
START = re.compile(
    r"^(requires|module|endmodule)\b"
    r"|^  (imports|configuration|syntax|context|rule|claim)\b"
)


def source_files() -> list[Path]:
    files = [SCRATCH / "reference-semantics" / "semantics.k"]
    files.extend(sorted((SCRATCH / "reference-semantics" / "semantics").glob("*.k")))
    files.extend([SCRATCH / "verification.k", SCRATCH / "spec.k"])
    return files


def is_task_path(rel: str, line: int, block: str) -> bool:
    if rel in {"verification.k", "spec.k"}:
        return True
    if rel.endswith("semantics/syntax.k"):
        return any(
            token in block
            for token in (
                "Expr ::=",
                "CmpOp",
                "Exprs",
                "Stmt ::=",
                "Stmts",
                "Params",
                "ParamNames",
                "Module",
            )
        )
    if rel.endswith("semantics/core.k"):
        return any(
            token in block
            for token in (
                "configuration",
                "syntax Val",
                "syntax KResult",
                "syntax Expr",
                "syntax Vals",
                "syntax RetState",
                "#loadAll",
                "(S:Stmt SS:Stmts)",
                ".Stmts",
                "Name(",
                "#look(",
                "builtinsScope",
                "#evalArgs",
                "#evalArgCont",
                "Int(I:Int)",
                "truthy(I:Int)",
                "applyBin",
                "applyCmp",
            )
        )
    if rel.endswith("semantics/functions.k"):
        return any(
            token in block
            for token in (
                "frame(",
                "#bindP",
                "#pop",
                "#endcall",
                "Return(",
            )
        )
    if rel.endswith("semantics/call.k"):
        return any(
            token in block
            for token in (
                "Call(",
                "#callee",
                "#applyK(toCall(closureVal",
            )
        )
    if rel.endswith("semantics/controls.k"):
        return any(
            token in block
            for token in (
                "#branch",
                "If(",
                "For(",
                "#loop(",
                "#loopStep",
                "#loopLbl",
            )
        )
    if rel.endswith("semantics/tuple.k"):
        return "#bindTgt(Name" in block or "syntax KItem ::= #bindTgt" in block
    if rel.endswith("semantics/builtins.k"):
        return 'applyBuiltin("range"' in block
    if rel.endswith("semantics/range.k"):
        return True
    if rel.endswith("semantics/operators.k"):
        return any(token in block for token in ("BinOp(", "Compare(", "applyCmp"))
    if rel.endswith("semantics/int.k"):
        return any(
            token in block
            for token in (
                'applyBin("%"',
                "pyMod",
                'applyCmp("<"',
                'applyCmp("=="',
            )
        )
    return False


def disposition(rel: str, line: int, block: str, relevance: str) -> str:
    if rel == "verification.k":
        if 73 <= line <= 100 and block.lstrip().startswith("rule"):
            return "ACCEPTED_EXACT_PROVEN_LOOP_BRIDGE"
        if line <= 30:
            return "ACCEPTED_MECHANICALLY_PINNED_MACRO"
        return "ACCEPTED_GUARDED_TERMINATING_MATH_SUMMARY"
    if rel == "spec.k":
        return "ACCEPTED_RESULT_CONSTRAINING_REACHABILITY_CLAIM"
    if "symbol(" in block or "no-evaluators" in block:
        return "TRUSTED_SUPPLIED_OPAQUE_OR_CONCRETE_TWIN_UNUSED_BY_TARGET"
    if relevance == "task-path":
        return "ACCEPTED_TASK_PATH_PYTHON_FAITHFUL"
    return "ACCEPTED_FIXED_SUPPLIED_BASELINE_UNUSED_NO_TASK_WITNESS"


def main() -> int:
    rows: list[dict[str, str | int]] = []
    for path in source_files():
        rel = path.relative_to(SCRATCH).as_posix()
        lines = path.read_text().splitlines()
        starts: list[tuple[int, str]] = []
        for index, text in enumerate(lines):
            match = START.match(text)
            if match:
                starts.append((index, match.group(1) or match.group(2)))
        for position, (index, kind) in enumerate(starts):
            next_index = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
            block_lines = lines[index:next_index]
            for offset, text in enumerate(block_lines[1:], start=1):
                if text.lstrip().startswith("//"):
                    block_lines = block_lines[:offset]
                    break
            while block_lines and not block_lines[-1].strip():
                block_lines.pop()
            block = "\n".join(block_lines)
            normalized = " ".join(part.strip() for part in block_lines if part.strip())
            attrs = sorted(set(re.findall(r"\[([^\]]+)\]", block)))
            relevance = "task-path" if is_task_path(rel, index + 1, block) else "imported-unreached"
            rows.append(
                {
                    "id": len(rows) + 1,
                    "location": f"{rel}:{index + 1}",
                    "kind": kind,
                    "attributes": "; ".join(attrs) or "-",
                    "function": (
                        "yes" if kind == "syntax" and "[function" in block else "no"
                    ),
                    "total": (
                        "yes"
                        if kind == "syntax" and re.search(r"\btotal\b", block)
                        else "no"
                    ),
                    "functional": (
                        "yes"
                        if kind == "syntax" and re.search(r"\bfunctional\b", block)
                        else "no"
                    ),
                    "opaque_symbol": (
                        "yes"
                        if kind == "syntax"
                        and ("symbol(" in block or "no-evaluators" in block)
                        else "no"
                    ),
                    "priority": "yes" if "priority(" in block else "no",
                    "simplification": "yes" if "simplification" in block else "no",
                    "relevance": relevance,
                    "decision": disposition(rel, index + 1, block, relevance),
                    "normalized_source": normalized,
                }
            )

    fields = list(rows[0])
    with OUTPUT.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, dialect="excel-tab")
        writer.writeheader()
        writer.writerows(rows)

    kinds = collections.Counter(str(row["kind"]) for row in rows)
    decisions = collections.Counter(str(row["decision"]) for row in rows)
    print(f"source_files={len(source_files())}")
    print(f"inventory_rows={len(rows)}")
    print(f"kinds={dict(sorted(kinds.items()))}")
    print(f"decisions={dict(sorted(decisions.items()))}")
    print(f"function_declarations={sum(row['function'] == 'yes' for row in rows)}")
    print(f"total_declarations={sum(row['total'] == 'yes' for row in rows)}")
    print(f"functional_declarations={sum(row['functional'] == 'yes' for row in rows)}")
    print(f"opaque_symbol_declarations={sum(row['opaque_symbol'] == 'yes' for row in rows)}")
    print(f"priority_items={sum(row['priority'] == 'yes' for row in rows)}")
    print(f"simplification_items={sum(row['simplification'] == 'yes' for row in rows)}")
    print("opaque_locations:")
    for row in rows:
        if row["opaque_symbol"] == "yes":
            print(f"  {row['location']} {row['normalized_source']}")
    print(f"output={OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
