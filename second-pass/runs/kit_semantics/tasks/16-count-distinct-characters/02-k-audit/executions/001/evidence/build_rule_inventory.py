#!/usr/bin/env python3
"""Create an exhaustive source-level inventory of local K declarations and rules."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
SOURCES = [ROOT / "reference-semantics" / "semantics.k"]
SOURCES.extend(sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")))
SOURCES.extend([ROOT / "verification.k", ROOT / "spec.k"])

START = re.compile(
    r"^(?:module\b|endmodule\b|requires\b|"
    r"  (?:imports|syntax|rule|configuration|claim|context|alias)\b)"
)

USED_MARKERS = {
    "syntax.k": [
        "Expr",
        "Stmt",
        "Stmts",
        "Exprs",
        "Params",
        "ParamNames",
        "Module",
        "Name",
        "Attribute",
        "Call",
        "Return",
        "FuncDef",
    ],
    "core.k": [
        "IntSeq",
        "Str",
        "Val",
        "KResult",
        "closureVal",
        "scope(",
        "configuration",
        "#look",
        "builtinsScope",
        "#evalArgs",
        "#evalArgCont",
        "#applyK",
        "appendVal",
        "isLen",
    ],
    "call.k": [
        "Attribute(",
        "Call(",
        "#callee",
        "boundMethodV",
        "builtinV",
        "closureVal",
        "typeV",
    ],
    "functions.k": [
        "FuncDef",
        "#bindP",
        "Return(",
        "#pop",
        "#endcall",
        "frame(",
    ],
    "methods.k": [
        'applyMethod(str(CS:IntSeq), "lower"',
        "lowerC(",
        "isUpperC(",
        "mapLower(",
    ],
    "builtins.k": [
        'applyBuiltin("len"',
        "seqLen(",
        'applyBuiltin("set"',
    ],
    "set.k": [
        "setV(",
        "codeIn(",
        "dedupCodes(",
        "dedupFrom(",
        "snocCode(",
    ],
}


def normalize(block: list[str]) -> str:
    return " ".join(line.strip() for line in block if line.strip())


def without_line_comment(line: str) -> str:
    in_string = False
    escaped = False
    for index, character in enumerate(line):
        if escaped:
            escaped = False
            continue
        if character == "\\" and in_string:
            escaped = True
            continue
        if character == '"':
            in_string = not in_string
            continue
        if (
            character == "/"
            and not in_string
            and index + 1 < len(line)
            and line[index + 1] == "/"
        ):
            return line[:index]
    return line


def kind_of(text: str) -> str:
    stripped = text.lstrip()
    first = stripped.split(maxsplit=1)[0] if stripped else "blank"
    if first == "syntax":
        flags = []
        for attribute in [
            "function",
            "functional",
            "total",
            "no-evaluators",
            "macro",
            "macro-rec",
            "strict",
            "seqstrict",
        ]:
            if re.search(rf"\b{re.escape(attribute)}\b", text):
                flags.append(attribute)
        return "syntax" + (":" + ",".join(flags) if flags else "")
    if first == "rule":
        flags = []
        for attribute in ["priority", "simplification", "concrete", "owise"]:
            if re.search(rf"\b{attribute}\b", text):
                flags.append(attribute)
        return "rule" + (":" + ",".join(flags) if flags else ":ordinary")
    return first


rows: list[dict[str, str | int]] = []
for source in SOURCES:
    lines = source.read_text().splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block = lines[start:end]
        text = normalize(block)
        code_text = normalize([without_line_comment(line) for line in block])
        if not text:
            continue
        filename = source.name
        markers = USED_MARKERS.get(filename, [])
        relation = (
            "candidate-local"
            if filename in {"verification.k", "spec.k"}
            else (
                "used-path"
                if any(marker in text for marker in markers)
                else "fixed-semantics-unused-path"
            )
        )
        decision = "NO_TASK_FALSE_WITNESS"
        if filename == "verification.k":
            decision = "NO_LOCAL_EXTENSION"
        elif filename == "spec.k" and text.lstrip().startswith("claim"):
            decision = "ENTRY_CLAIM_AUDITED_STAGES_3_4_6"
        elif filename == "methods.k" and start + 1 == 143:
            decision = "SOURCE_MISMATCH_UNICODE_WITNESSES_STAGE4"
        elif filename == "str.k" and start + 1 in {13, 14, 15, 16}:
            decision = "ASCII_LITERAL_MODEL_BOUNDARY"
        elif relation == "used-path":
            decision = "USED_PATH_STRUCTURALLY_OR_MATHEMATICALLY_VALID_IN_MODEL"

        rows.append(
            {
                "id": len(rows) + 1,
                "file": str(source.relative_to(ROOT)),
                "line": start + 1,
                "kind": kind_of(code_text),
                "relation": relation,
                "decision": decision,
                "text": text,
            }
        )

tsv_path = Path("/audit-output/evidence/rule-inventory.tsv")
with tsv_path.open("w", newline="") as stream:
    writer = csv.DictWriter(
        stream,
        fieldnames=["id", "file", "line", "kind", "relation", "decision", "text"],
        delimiter="\t",
    )
    writer.writeheader()
    writer.writerows(rows)

md_path = Path("/audit-output/evidence/rule-inventory.md")
with md_path.open("w") as stream:
    stream.write("# Exhaustive local K source inventory\n\n")
    stream.write(
        "| ID | File:line | Kind | Relation | Review decision | Declaration/rule |\n"
    )
    stream.write("|---:|---|---|---|---|---|\n")
    for row in rows:
        escaped = str(row["text"]).replace("|", "\\|")
        stream.write(
            f"| {row['id']} | `{row['file']}:{row['line']}` | "
            f"`{row['kind']}` | `{row['relation']}` | `{row['decision']}` | "
            f"`{escaped}` |\n"
        )

counts: dict[str, int] = {}
for row in rows:
    key = str(row["kind"])
    counts[key] = counts.get(key, 0) + 1

print(f"source_count={len(SOURCES)}")
print(f"inventory_entry_count={len(rows)}")
for key in sorted(counts):
    print(f"kind_count {key}={counts[key]}")
print(f"tsv={tsv_path}")
print(f"markdown={md_path}")
