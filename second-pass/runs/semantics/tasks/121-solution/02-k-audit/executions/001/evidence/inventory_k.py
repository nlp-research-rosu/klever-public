#!/usr/bin/env python3
"""Emit a complete line-addressed inventory of local K declarations."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


START = re.compile(r"^\s{2}(configuration|syntax|context|rule|claim|alias)\b")
MODULE = re.compile(r"^\s*module\s+(\S+)")
ENDMODULE = re.compile(r"^\s*endmodule\b")
ATTR_NAMES = (
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
)

EXECUTION_FILES = {
    "syntax.k",
    "core.k",
    "iter.k",
    "list.k",
    "tuple.k",
    "operators.k",
    "int.k",
    "bool.k",
    "controls.k",
    "functions.k",
    "call.k",
}
EXECUTION_TOKENS = {
    "Module",
    "FuncDef",
    "Params",
    "Assign",
    "Name",
    "Int",
    "Bool",
    "For",
    "If",
    "Return",
    "UnaryOp",
    "BinOp",
    "Call",
    "ValSeq",
    "list",
    "closureVal",
    "#loadAll",
    "#look",
    "#evalArgs",
    "truthy",
    "applyUn",
    "applyBin",
    "#iterNext",
    "#loop",
    "#branch",
    "#bindTgt",
    "#bindP",
    "#applyK",
    "#callee",
    "#endcall",
    "#pop",
    "pyMod",
}


def normalize(lines: list[str]) -> str:
    kept = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("//"):
            kept.append(stripped)
    return " ".join(" ".join(kept).split())


def classify(path: Path, kind: str, text: str) -> tuple[str, str]:
    if path.name == "verification.k":
        return "PROOF_LOCAL", "INDIVIDUALLY_REVIEWED_IN_REVIEW_MD"
    if path.name == "spec.k":
        return "TARGET_CLAIM", "INDIVIDUALLY_REVIEWED_IN_REVIEW_MD"
    if path.name == "concrete.k":
        return "CONCRETE_ONLY", "INERT_NOT_IMPORTED_BY_HASKELL_PROOF"
    if path.name not in EXECUTION_FILES:
        return "IMPORTED_DORMANT", "INERT_FOR_SUBMITTED_PROGRAM_NO_FALSE_WITNESS"
    if any(token in text for token in EXECUTION_TOKENS):
        return "EXECUTION_SLICE", "ACCEPTED_FIXED_BASELINE_NO_FALSE_WITNESS"
    return "IMPORTED_DORMANT", "INERT_FOR_SUBMITTED_PROGRAM_NO_FALSE_WITNESS"


def inventory_file(path: Path) -> list[dict[str, str | int]]:
    lines = path.read_text().splitlines()
    records: list[dict[str, str | int]] = []
    module = ""
    starts: list[tuple[int, str, str]] = []
    current_module = ""
    for index, line in enumerate(lines):
        module_match = MODULE.match(line)
        if module_match:
            current_module = module_match.group(1)
        match = START.match(line)
        if match:
            starts.append((index, match.group(1), current_module))
        if ENDMODULE.match(line):
            current_module = ""

    boundaries = [index for index, _, _ in starts] + [len(lines)]
    for ordinal, (start, kind, record_module) in enumerate(starts):
        end = boundaries[ordinal + 1]
        while end > start + 1 and (
            not lines[end - 1].strip()
            or lines[end - 1].lstrip().startswith("//")
            or ENDMODULE.match(lines[end - 1])
        ):
            end -= 1
        text = normalize(lines[start:end])
        attrs = [name for name in ATTR_NAMES if re.search(rf"\b{re.escape(name)}\b", text)]
        role, decision = classify(path, kind, text)
        if kind == "rule":
            if "<" in text and ">" in text:
                subtype = "operational-rule"
            elif "macro" in text:
                subtype = "macro-equation"
            else:
                subtype = "equational-rule"
        elif kind == "syntax" and "no-evaluators" in attrs:
            subtype = "opaque-symbol-declaration"
        else:
            subtype = kind
        records.append(
            {
                "file": str(path),
                "module": record_module,
                "start": start + 1,
                "end": end,
                "kind": kind,
                "subtype": subtype,
                "attributes": ",".join(attrs) if attrs else "-",
                "proof_role": role,
                "decision": decision,
                "text": text.replace("\t", " "),
            }
        )
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args()
    records = []
    for path in args.files:
        records.extend(inventory_file(path))

    columns = [
        "file",
        "module",
        "start",
        "end",
        "kind",
        "subtype",
        "attributes",
        "proof_role",
        "decision",
        "text",
    ]
    print("\t".join(columns))
    for record in records:
        print("\t".join(str(record[column]) for column in columns))

    kinds: dict[str, int] = {}
    attributes: dict[str, int] = {}
    roles: dict[str, int] = {}
    for record in records:
        kinds[str(record["kind"])] = kinds.get(str(record["kind"]), 0) + 1
        roles[str(record["proof_role"])] = roles.get(str(record["proof_role"]), 0) + 1
        for attribute in str(record["attributes"]).split(","):
            if attribute != "-":
                attributes[attribute] = attributes.get(attribute, 0) + 1
    print(f"# TOTAL_RECORDS={len(records)}")
    print("# KINDS=" + ",".join(f"{key}:{kinds[key]}" for key in sorted(kinds)))
    print("# ATTRIBUTES=" + ",".join(f"{key}:{attributes[key]}" for key in sorted(attributes)))
    print("# ROLES=" + ",".join(f"{key}:{roles[key]}" for key in sorted(roles)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
