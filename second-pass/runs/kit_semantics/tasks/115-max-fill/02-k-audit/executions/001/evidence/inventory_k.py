#!/usr/bin/env python3
"""Exhaustive declaration/rule inventory for the audited K source files."""

from pathlib import Path
import re


ROOT = Path("/reference/reference-semantics")
FILES = [ROOT / "semantics.k", *sorted((ROOT / "semantics").glob("*.k"))]
FILES += [Path("/candidate/verification.k"), Path("/candidate/spec.k")]

START = re.compile(
    r"^\s*(module|endmodule|imports|configuration|syntax|context|rule|claim)\b"
)

# Source lines that can execute or directly define values on the submitted
# max_fill target path.  Broader supplied modules remain inventoried as inert
# for this target, rather than silently omitted.
MATERIAL_RANGES = {
    "semantics.k": [(34, 80)],
    "semantics/syntax.k": [
        (9, 15),
        (28, 30),
        (41, 45),
        (50, 61),
    ],
    "semantics/core.k": [
        (13, 70),
        (117, 127),
        (129, 225),
    ],
    "semantics/iter.k": [(6, 9)],
    "semantics/operators.k": [(6, 17), (22, 31)],
    "semantics/int.k": [(4, 20)],
    "semantics/list.k": [(3, 15)],
    "semantics/tuple.k": [(30, 41)],
    "semantics/controls.k": [(3, 31), (62, 75), (93, 108)],
    "semantics/functions.k": [(3, 20), (62, 91)],
    "semantics/builtins.k": [(3, 17), (46, 56)],
    "semantics/call.k": [(10, 50), (69, 75)],
}


def relative(path):
    if path.is_relative_to(ROOT):
        return str(path.relative_to(ROOT))
    return str(path)


def is_material(rel, line):
    return any(lo <= line <= hi for lo, hi in MATERIAL_RANGES.get(rel, []))


def flatten(block):
    return " ".join(
        part.strip()
        for part in block.splitlines()
        if part.strip() and not part.lstrip().startswith("//")
    )


records = []
for path in FILES:
    lines = path.read_text().splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    for pos, (index, kind) in enumerate(starts):
        end = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        block = flatten("\n".join(lines[index:end]))
        rel = relative(path)
        line_no = index + 1
        attrs = []
        for attr in (
            "function",
            "functional",
            "total",
            "symbol",
            "no-evaluators",
            "simplification",
            "priority",
            "owise",
            "concrete",
            "symbolic",
            "macro",
            "macro-rec",
            "strict",
            "seqstrict",
        ):
            if re.search(rf"\b{re.escape(attr)}\b", block):
                attrs.append(attr)

        if kind == "syntax":
            subtype = "syntax"
            if "function" in attrs or "functional" in attrs:
                subtype = "function-declaration"
            if "no-evaluators" in attrs:
                subtype = "opaque-function-declaration"
        elif kind == "rule":
            subtype = "ordinary-rule"
            if "simplification" in attrs:
                subtype = "simplification-rule"
            elif "macro" in attrs or "macro-rec" in attrs:
                subtype = "macro-rule"
            elif "priority" in attrs:
                subtype = "priority-rule"
            elif "concrete" in attrs:
                subtype = "concrete-rule"
        else:
            subtype = kind

        material = is_material(rel, line_no)
        if str(path).endswith("/candidate/verification.k"):
            scope = "PROOF_LOCAL"
            decision = "ACCEPTED_PROOF_LOCAL_MANUAL_STAGE5"
            material = True
        elif str(path).endswith("/candidate/spec.k"):
            scope = "CLAIM"
            decision = "AUDITED_FOR_ADEQUACY_STAGE4"
            material = True
        else:
            scope = "SUPPLIED_FIXED"
            decision = (
                "ACCEPTED_FIXED_TARGET_PATH"
                if material
                else "ACCEPTED_INERT_FOR_TARGET"
            )

        records.append(
            {
                "path": rel,
                "line": line_no,
                "kind": subtype,
                "attrs": ",".join(attrs) or "-",
                "scope": scope,
                "material": "YES" if material else "NO",
                "decision": decision,
                "text": block,
            }
        )

print(
    "path\tline\tkind\tattributes\tscope\tmaterial_to_max_fill"
    "\treviewer_disposition\tdeclaration_or_rule"
)
for record in records:
    print(
        "{path}\t{line}\t{kind}\t{attrs}\t{scope}\t{material}\t"
        "{decision}\t{text}".format(**record)
    )

print()
print(f"FILES={len(FILES)}")
print(f"RECORDS={len(records)}")
for kind in sorted({record["kind"] for record in records}):
    count = sum(record["kind"] == kind for record in records)
    print(f"KIND_COUNT {kind} {count}")
for scope in ("SUPPLIED_FIXED", "PROOF_LOCAL", "CLAIM"):
    count = sum(record["scope"] == scope for record in records)
    print(f"SCOPE_COUNT {scope} {count}")
print(
    "MATERIAL_FIXED_RECORDS="
    + str(
        sum(
            record["scope"] == "SUPPLIED_FIXED"
            and record["material"] == "YES"
            for record in records
        )
    )
)
