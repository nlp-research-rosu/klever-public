#!/usr/bin/env python3
"""Build an exhaustive declaration/rule ledger from the audited K sources."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path("/tmp/audit-work/candidate")
SEMANTICS = ROOT / "reference-semantics"
OUTPUT = Path("/audit-output/evidence/rule_inventory.md")
START = re.compile(r"^\s*(syntax|configuration|context|rule|claim)\b")


# Rules/declarations on the actual solution.mpy execution slice. All remaining
# supplied-semantics entries are inventoried as out of slice, not silently
# omitted.
USED_FIXED = {
    ("reference-semantics/semantics/core.k", 125),
    ("reference-semantics/semantics/core.k", 126),
    ("reference-semantics/semantics/core.k", 127),
    ("reference-semantics/semantics/core.k", 131),
    ("reference-semantics/semantics/core.k", 132),
    ("reference-semantics/semantics/core.k", 152),
    ("reference-semantics/semantics/core.k", 158),
    ("reference-semantics/semantics/core.k", 189),
    ("reference-semantics/semantics/core.k", 190),
    ("reference-semantics/semantics/core.k", 191),
    ("reference-semantics/semantics/core.k", 194),
    ("reference-semantics/semantics/core.k", 214),
    ("reference-semantics/semantics/core.k", 215),
    ("reference-semantics/semantics/call.k", 20),
    ("reference-semantics/semantics/call.k", 21),
    ("reference-semantics/semantics/call.k", 31),
    ("reference-semantics/semantics/call.k", 32),
    ("reference-semantics/semantics/call.k", 69),
    ("reference-semantics/semantics/functions.k", 14),
    ("reference-semantics/semantics/functions.k", 63),
    ("reference-semantics/semantics/functions.k", 64),
    ("reference-semantics/semantics/functions.k", 78),
    ("reference-semantics/semantics/functions.k", 85),
    ("reference-semantics/semantics/controls.k", 9),
    ("reference-semantics/semantics/operators.k", 12),
    ("reference-semantics/semantics/operators.k", 17),
    ("reference-semantics/semantics/builtins.k", 44),
    ("reference-semantics/semantics/builtins.k", 140),
    ("reference-semantics/semantics/float.k", 31),
    ("reference-semantics/semantics/float.k", 32),
    ("reference-semantics/semantics/float.k", 120),
    ("reference-semantics/semantics/float.k", 121),
    ("reference-semantics/semantics/float.k", 132),
    ("reference-semantics/semantics/float.k", 196),
    ("reference-semantics/semantics/float.k", 210),
    ("reference-semantics/semantics/float.k", 211),
    ("reference-semantics/semantics/float.k", 218),
    ("reference-semantics/semantics/float.k", 227),
    ("reference-semantics/semantics/int.k", 17),
    ("reference-semantics/semantics/int.k", 26),
}

USED_FIXED_DECLARATIONS = {
    ("reference-semantics/semantics/syntax.k", 9),
    ("reference-semantics/semantics/syntax.k", 32),
    ("reference-semantics/semantics/syntax.k", 37),
    ("reference-semantics/semantics/syntax.k", 41),
    ("reference-semantics/semantics/syntax.k", 56),
    ("reference-semantics/semantics/syntax.k", 57),
    ("reference-semantics/semantics/syntax.k", 60),
    ("reference-semantics/semantics/syntax.k", 61),
    ("reference-semantics/semantics/core.k", 25),
    ("reference-semantics/semantics/core.k", 36),
    ("reference-semantics/semantics/core.k", 37),
    ("reference-semantics/semantics/core.k", 38),
    ("reference-semantics/semantics/core.k", 39),
    ("reference-semantics/semantics/core.k", 40),
    ("reference-semantics/semantics/core.k", 41),
    ("reference-semantics/semantics/core.k", 42),
    ("reference-semantics/semantics/core.k", 49),
    ("reference-semantics/semantics/core.k", 124),
    ("reference-semantics/semantics/core.k", 130),
    ("reference-semantics/semantics/core.k", 157),
    ("reference-semantics/semantics/core.k", 185),
    ("reference-semantics/semantics/core.k", 186),
    ("reference-semantics/semantics/core.k", 208),
    ("reference-semantics/semantics/core.k", 209),
    ("reference-semantics/semantics/core.k", 210),
    ("reference-semantics/semantics/core.k", 213),
    ("reference-semantics/semantics/call.k", 19),
    ("reference-semantics/semantics/functions.k", 8),
    ("reference-semantics/semantics/float.k", 20),
    ("reference-semantics/semantics/float.k", 30),
    ("reference-semantics/semantics/float.k", 119),
    ("reference-semantics/semantics/float.k", 195),
    ("reference-semantics/semantics/float.k", 209),
    ("reference-semantics/semantics/float.k", 217),
    ("reference-semantics/semantics/builtins.k", 17),
}

VERIFICATION_DECISIONS = {
    10: (
        "REJECTED result-bearing abstract values: oneThirdV/cubeRootV are "
        "program-derived and have no bridge-free value theorem."
    ),
    11: (
        "REJECTED result-bearing opaque total function: roundedCubeRoot has no "
        "defining equations or bridge-free connection theorem."
    ),
    14: (
        "REJECTED operational bridge: priority 40 preempts fixed divII(1,3); "
        "no universal value-equivalence theorem."
    ),
    15: (
        "REJECTED operational bridge: replaces fixed Float exponentiation with "
        "cubeRootV(I), without value equivalence."
    ),
    16: (
        "REJECTED operational bridge: replaces fixed roundF with "
        "roundedCubeRoot(I), without value equivalence."
    ),
    22: "ACCEPTED guarded integer identity: N>=0 implies abs(N^3)=N^3.",
    25: "ACCEPTED guarded integer identity: N>0 implies abs(-N^3)=N^3.",
    28: (
        "ACCEPTED guarded integer identity: N>=0,D>0 implies "
        "abs(N^3+D)=N^3+D."
    ),
    32: (
        "ACCEPTED guarded integer identity: N>=0,D>0 implies "
        "abs(-(N^3+D))=N^3+D."
    ),
    41: (
        "REJECTED answer axiom and false real-program conclusion. Witness "
        "N=10^15: the rule says the comparison is true for 10^45, while "
        "CPython and fixed supplied-semantics execution return false. Also "
        "false under the admissible interpretation roundedCubeRoot(1)=0."
    ),
    48: (
        "ACCEPTED as integer mathematics in isolation: the guards put N^3+D "
        "strictly between consecutive cubes, so no integer cubed equals it. "
        "Its use does not repair the rejected operational bridges."
    ),
    59: (
        "ACCEPTED total definitional symbol: one exhaustive rule defines "
        "iscubeClosure; constructor comparison pins it to solution.mpy."
    ),
    60: (
        "ACCEPTED definitional summary: exact function body, parameters, and "
        "module defining scope, mechanically checked."
    ),
}

SPEC_DECISIONS = {
    7: (
        "REJECTED as a real-program theorem: result is constrained but circularly "
        "uses the same unconnected roundedCubeRoot abstraction introduced by execution."
    ),
    30: (
        "REJECTED false real-program claim. Satisfying witness N=10^15 gives "
        "input 10^45; actual candidate/fixed semantics return false, not true."
    ),
    50: (
        "REJECTED false real-program claim. Satisfying witness N=10^15 gives "
        "input -10^45; abs leads to the same actual false result."
    ),
    70: (
        "Conclusion is valid integer non-cube mathematics, but closure depends "
        "on rejected execution bridges and is not an independent real-program proof."
    ),
    92: (
        "Conclusion is valid integer non-cube mathematics, but closure depends "
        "on rejected execution bridges and is not an independent real-program proof."
    ),
}


def attributes(statement: str) -> str:
    flags = []
    for flag in [
        "function",
        "functional",
        "total",
        "symbol",
        "no-evaluators",
        "priority",
        "simplification",
        "concrete",
        "owise",
        "strict",
        "seqstrict",
        "macro",
        "macro-rec",
    ]:
        if re.search(rf"\b{re.escape(flag)}\b", statement):
            flags.append(flag)
    return ", ".join(flags) if flags else "—"


def flatten(block: list[str]) -> str:
    retained = []
    for raw in block:
        stripped = raw.strip()
        if not stripped or stripped.startswith("//"):
            continue
        if stripped.startswith(("module ", "endmodule", "imports ")):
            continue
        retained.append(stripped)
    return " ".join(retained)


def decision(relative: str, line: int, kind: str, statement: str) -> str:
    if relative == "verification.k":
        return VERIFICATION_DECISIONS.get(
            line, "REVIEW ERROR: unclassified proof-local declaration/rule"
        )
    if relative == "spec.k":
        return SPEC_DECISIONS.get(line, "REVIEW ERROR: unclassified entry claim")
    if relative.startswith("reference-semantics/"):
        key = (relative, line)
        if key in USED_FIXED or key in USED_FIXED_DECLARATIONS:
            if "no-evaluators" in statement:
                return (
                    "FIXED-SEMANTICS OPAQUE/CONCRETE BOUNDARY on the executed "
                    "slice; concrete rule is authoritative for krun, but Haskell "
                    "cannot establish its value symbolically."
                )
            return (
                "ACCEPTED FIXED-SEMANTICS ENTRY on the executed slice; "
                "constructor/control/value behavior was checked against the "
                "program path. No false conclusion witness identified."
            )
        if kind == "rule":
            return (
                "OUTSIDE EXECUTED SLICE. Fixed supplied-semantics rule; no "
                "candidate proof dependence and no false conclusion witness identified."
            )
        if "no-evaluators" in statement:
            return (
                "OUTSIDE EXECUTED SLICE. Opaque fixed-semantics declaration; "
                "does not affect this proof."
            )
        return (
            "DECLARATION/CONTEXT OUTSIDE EXECUTED SLICE or structural support; "
            "attributes inventoried and no candidate proof dependence."
        )
    return "REVIEW ERROR: unknown source"


def records_for(path: Path):
    lines = path.read_text().splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    records = []
    for position, (index, kind) in enumerate(starts):
        stop = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        statement = flatten(lines[index:stop])
        records.append((index + 1, kind, statement))
    return records


def escape_cell(text: str) -> str:
    return text.replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def main() -> int:
    files = sorted(SEMANTICS.rglob("*.k")) + [ROOT / "verification.k", ROOT / "spec.k"]
    all_records = []
    per_file = defaultdict(Counter)
    attr_counts = Counter()
    errors = []
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        for line, kind, statement in records_for(path):
            attrs = attributes(statement)
            verdict = decision(relative, line, kind, statement)
            if verdict.startswith("REVIEW ERROR"):
                errors.append(f"{relative}:{line}: {verdict}")
            all_records.append((relative, line, kind, attrs, statement, verdict))
            per_file[relative][kind] += 1
            for attr in attrs.split(", "):
                if attr != "—":
                    attr_counts[attr] += 1

    output = []
    output.append("# Exhaustive K declaration and rule inventory")
    output.append("")
    output.append(
        "Generated from the clean scratch source tree. Each declaration, "
        "configuration, context, semantic rule, proof-local rule, and claim "
        "start is listed once with attributes and an audit decision."
    )
    output.append("")
    output.append(f"Total inventory entries: **{len(all_records)}**")
    output.append("")
    output.append("## Counts by file")
    output.append("")
    output.append("| File | Syntax | Configuration | Context | Rule | Claim |")
    output.append("|---|---:|---:|---:|---:|---:|")
    for relative in sorted(per_file):
        counts = per_file[relative]
        output.append(
            f"| {escape_cell(relative)} | {counts['syntax']} | "
            f"{counts['configuration']} | {counts['context']} | "
            f"{counts['rule']} | {counts['claim']} |"
        )
    output.append("")
    output.append("## Attribute occurrence counts")
    output.append("")
    output.append("| Attribute | Inventory entries containing it |")
    output.append("|---|---:|")
    for attr, count in sorted(attr_counts.items()):
        output.append(f"| {attr} | {count} |")
    output.append("")
    output.append("## Entry-by-entry ledger")
    output.append("")
    output.append("| Location | Kind | Attributes | Declaration/rule | Decision |")
    output.append("|---|---|---|---|---|")
    for relative, line, kind, attrs, statement, verdict in all_records:
        output.append(
            f"| {escape_cell(relative)}:{line} | {kind} | "
            f"{escape_cell(attrs)} | {escape_cell(statement)} | "
            f"{escape_cell(verdict)} |"
        )
    output.append("")
    output.append(f"Classification errors: **{len(errors)}**")
    for error in errors:
        output.append(f"- {error}")
    output.append("")
    OUTPUT.write_text("\n".join(output))
    print(f"OUTPUT={OUTPUT}")
    print(f"FILES_SCANNED={len(files)}")
    print(f"ENTRIES={len(all_records)}")
    print(f"RULES={sum(1 for record in all_records if record[2] == 'rule')}")
    print(f"SYNTAX={sum(1 for record in all_records if record[2] == 'syntax')}")
    print(f"CONTEXTS={sum(1 for record in all_records if record[2] == 'context')}")
    print(
        "CONFIGURATIONS="
        f"{sum(1 for record in all_records if record[2] == 'configuration')}"
    )
    print(f"CLAIMS={sum(1 for record in all_records if record[2] == 'claim')}")
    print(f"ATTRIBUTE_COUNTS={dict(sorted(attr_counts.items()))}")
    print(f"CLASSIFICATION_ERRORS={len(errors)}")
    for error in errors:
        print(f"ERROR={error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
