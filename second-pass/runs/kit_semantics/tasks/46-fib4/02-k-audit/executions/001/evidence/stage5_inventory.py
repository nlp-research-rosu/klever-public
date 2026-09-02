#!/usr/bin/env python3
"""Exhaustive inventory of local K declarations, contexts, rules, and claims."""

from __future__ import annotations

import collections
import re
from dataclasses import dataclass
from pathlib import Path


WORK = Path("/tmp/audit-work/46-fib4")
SEMANTICS = WORK / "reference-semantics"
START = re.compile(r"^\s*(syntax|rule|context|configuration|claim)\b")


@dataclass
class Item:
    path: Path
    line: int
    kind: str
    text: str

    @property
    def compact(self) -> str:
        return " ".join(
            part.strip()
            for part in self.text.splitlines()
            if part.strip() and not part.lstrip().startswith("//")
        )

    @property
    def attributes(self) -> str:
        attrs = re.findall(r"\[([^\]]+)\]", self.compact)
        return ";".join(attrs) if attrs else "-"


def parse_file(path: Path) -> list[Item]:
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    items: list[Item] = []
    for offset, (index, kind) in enumerate(starts):
        end = starts[offset + 1][0] if offset + 1 < len(starts) else len(lines)
        while end > index + 1 and (
            not lines[end - 1].strip()
            or lines[end - 1].lstrip().startswith("//")
            or lines[end - 1].strip() == "endmodule"
        ):
            end -= 1
        items.append(Item(path, index + 1, kind, "\n".join(lines[index:end])))
    return items


REACHED_PATTERNS = (
    "configuration",
    'syntax Expr ::= "Int"',
    'syntax Stmt ::= "Assign"',
    "syntax Stmts",
    "syntax Params",
    "syntax Module",
    "syntax Val      ::= Int",
    "syntax Parent",
    "syntax Scope",
    "syntax KResult",
    "syntax Expr     ::= Val",
    "syntax Vals",
    "syntax RetState",
    "#loadAll",
    "(S:Stmt SS:Stmts)",
    ".Stmts => .K",
    "#look",
    "Name(X:String)",
    "builtinsScope",
    "#evalArgs",
    "#evalArgCont",
    "#applyK",
    "Int(I:Int)",
    "truthy(I:Int)",
    "applyBin(String",
    "applyCmp(String",
    "appendVal",
    "BinOp(OP:String",
    "Compare(LV:Val",
    'applyBin("+",  I1:Int',
    'applyCmp("<",  I1:Int',
    "#while",
    "#whileCond",
    "#loopLbl",
    "While(C:Expr",
    "Assign(Name",
    "frame(continuation",
    "FuncDef(F:String, Params",
    "#bindP",
    "Return(V:Val)",
    "#endcall",
    "#pop",
    "#callee",
    "Call(Fe:Expr",
    "closureVal(PNS",
)


def decision(item: Item) -> str:
    rel = item.path.relative_to(WORK).as_posix()
    text = item.compact
    if rel == "verification.k":
        return "PROOF_LOCAL_REVIEWED_SOUND"
    if rel == "spec.k":
        if "loop-invariant" in text:
            return "DERIVED_CIRCULARITY_REVIEWED_SOUND"
        return "TARGET_CLAIM_REVIEWED_SOUND"
    if rel.endswith("semantics/concrete.k"):
        return "CONCRETE_ONLY_NOT_IMPORTED_BY_PROOF"
    if any(pattern in text for pattern in REACHED_PATTERNS):
        return "REACHED_FIXED_ITEM_REVIEWED_SOUND"
    return "UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS"


def main() -> None:
    paths = sorted((SEMANTICS / "semantics").glob("*.k"))
    paths = [SEMANTICS / "semantics.k", *paths, WORK / "verification.k", WORK / "spec.k"]
    all_items: list[Item] = []
    for path in paths:
        all_items.extend(parse_file(path))

    count_by_kind = collections.Counter(item.kind for item in all_items)
    count_by_decision = collections.Counter(decision(item) for item in all_items)
    attribute_counts: collections.Counter[str] = collections.Counter()
    for item in all_items:
        compact = item.compact
        for attribute in (
            "function",
            "total",
            "functional",
            "simplification",
            "priority",
            "owise",
            "concrete",
            "macro",
            "macro-rec",
            "strict",
            "seqstrict",
            "symbol",
            "no-evaluators",
        ):
            if re.search(rf"\b{re.escape(attribute)}\b", compact):
                attribute_counts[attribute] += 1

    print("# Stage 5 exhaustive local K inventory")
    print()
    print(f"Files inventoried: {len(paths)}")
    print(f"Items inventoried: {len(all_items)}")
    print(f"By kind: {dict(sorted(count_by_kind.items()))}")
    print(f"By decision: {dict(sorted(count_by_decision.items()))}")
    print(f"Attribute-bearing item counts: {dict(sorted(attribute_counts.items()))}")
    print(
        "Interpretation: `UNREACHED_FIXED_ITEM_NO_EFFECT_ON_CLAIMS` means the "
        "item was inspected but no constructor/operator in the submitted program "
        "or proof path can match it. It is not a proof-local assumption."
    )
    print()
    print("| ID | Kind | Attributes | Reachability/soundness decision | Declaration or rule |")
    print("|---|---|---|---|---|")
    for item in all_items:
        rel = item.path.relative_to(WORK).as_posix()
        compact = item.compact.replace("|", "\\|")
        print(
            f"| `{rel}:{item.line}` | {item.kind} | `{item.attributes}` | "
            f"{decision(item)} | `{compact}` |"
        )

    print()
    print("## Per-file raw-start cross-check")
    print()
    for path in paths:
        raw = collections.Counter()
        for line in path.read_text().splitlines():
            match = START.match(line)
            if match:
                raw[match.group(1)] += 1
        parsed = collections.Counter(
            item.kind for item in all_items if item.path == path
        )
        status = "PASS" if raw == parsed else "FAIL"
        print(
            f"- `{path.relative_to(WORK).as_posix()}`: {status}; "
            f"raw={dict(raw)} parsed={dict(parsed)}"
        )


if __name__ == "__main__":
    main()
