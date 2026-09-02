#!/usr/bin/env python3
"""Lexical inventory of every local K sentence used by the reconstructed proof."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


WORK = Path("/tmp/audit-work/122-add-elements-audit")
EVIDENCE = Path("/audit-output/evidence")
KEYWORDS = {
    "imports",
    "syntax",
    "configuration",
    "rule",
    "claim",
    "context",
    "alias",
}
OUTER_RE = re.compile(
    r"^(?P<indent>[ \t]*)(?P<keyword>"
    + "|".join(sorted(KEYWORDS))
    + r")\b"
)
MODULE_RE = re.compile(r"^[ \t]*module[ \t]+(?P<name>[A-Za-z][A-Za-z0-9_-]*)")
ENDMODULE_RE = re.compile(r"^[ \t]*endmodule\b")
ATTRIBUTE_RE = re.compile(r"\[([^\[\]]*)\]")


PROOF_RULE_ASSESSMENTS = {
    7: (
        "definitional-summary",
        "Sound base equation for the empty ValSeq.",
    ),
    8: (
        "definitional-summary",
        "Sound structural integer predicate; recursive descent is strict.",
    ),
    15: (
        "definitional-summary",
        "Identity projection is sound on Int. The [total] declaration is "
        "not covered for non-Int Val constructors, but every result-bearing "
        "use is guarded by isInt.",
    ),
    16: (
        "definitional-summary",
        "Sound empty-sequence accumulator equation.",
    ),
    17: (
        "definitional-summary",
        "Sound inclusion branch for integer values with abs(value) < 100.",
    ),
    20: (
        "definitional-summary",
        "Sound exclusion branch; disjoint from and complete with the <100 "
        "branch for integer values.",
    ),
    27: (
        "derived-lemma",
        "Refined-sort form of the supplied integer abs rule; value and "
        "control agree under isInt.",
    ),
    31: (
        "derived-lemma",
        "Refined-sort form of supplied integer addition; value and control "
        "agree under isInt.",
    ),
    39: (
        "derived-lemma",
        "Sound MAP update key-membership equation at the updated key.",
    ),
    41: (
        "derived-lemma",
        "Sound MAP update key-membership equation for a distinct key.",
    ),
    45: (
        "derived-lemma",
        "Sound MAP lookup equation at the updated key.",
    ),
    47: (
        "derived-lemma",
        "Sound MAP lookup equation for a distinct key.",
    ),
    54: (
        "operational-bridge",
        "Truthful specialization of supplied positive-step slice adjustment. "
        "No bridge-free machine-checked universal connection theorem is "
        "provided.",
    ),
    61: (
        "operational-bridge",
        "Truthful prefix extraction specialization of supplied buildVS "
        "recursion. No bridge-free machine-checked universal connection "
        "theorem is provided.",
    ),
}


def mask_comments(text: str) -> str:
    output = list(text)
    index = 0
    state = "code"
    block_depth = 0
    while index < len(text):
        char = text[index]
        following = text[index + 1] if index + 1 < len(text) else ""
        if state == "line":
            if char in "\r\n":
                state = "code"
            else:
                output[index] = " "
            index += 1
            continue
        if state == "string":
            if char == "\\" and following:
                output[index] = output[index + 1] = " "
                index += 2
                continue
            if char == '"':
                state = "code"
            elif char not in "\r\n":
                output[index] = " "
            index += 1
            continue
        if state == "block":
            if char == "/" and following == "*":
                output[index] = output[index + 1] = " "
                block_depth += 1
                index += 2
                continue
            if char == "*" and following == "/":
                output[index] = output[index + 1] = " "
                block_depth -= 1
                index += 2
                if block_depth == 0:
                    state = "code"
                continue
            if char not in "\r\n":
                output[index] = " "
            index += 1
            continue
        if char == "/" and following == "/":
            output[index] = output[index + 1] = " "
            state = "line"
            index += 2
            continue
        if char == "/" and following == "*":
            output[index] = output[index + 1] = " "
            state = "block"
            block_depth = 1
            index += 2
            continue
        if char == '"':
            state = "string"
        index += 1
    return "".join(output)


def attributes(text: str) -> list[str]:
    result = []
    for match in ATTRIBUTE_RE.finditer(mask_comments(text)):
        for token in match.group(1).split(","):
            token = token.strip()
            if token:
                result.append(token)
    return result


def scan_file(path: Path, origin: str) -> list[dict[str, object]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    masked_lines = mask_comments(text).splitlines(keepends=True)
    module = None
    starts: list[tuple[int, str, str | None]] = []

    for index, masked_line in enumerate(masked_lines, start=1):
        stripped = masked_line.rstrip("\r\n")
        module_match = MODULE_RE.match(stripped)
        if module_match:
            module = module_match.group("name")
            continue
        if ENDMODULE_RE.match(stripped):
            module = None
            continue
        match = OUTER_RE.match(stripped)
        if match and module is not None:
            indent = match.group("indent").replace("\t", "    ")
            if len(indent) <= 2:
                starts.append((index, match.group("keyword"), module))
        elif (
            module is None
            and stripped.startswith("requires ")
            and not stripped.startswith((" ", "\t"))
        ):
            starts.append((index, "requires-file", None))

    records = []
    for position, (start_line, keyword, sentence_module) in enumerate(starts):
        end_line = (
            starts[position + 1][0] - 1
            if position + 1 < len(starts)
            else len(lines)
        )
        while end_line >= start_line and not lines[end_line - 1].strip():
            end_line -= 1
        sentence_text = "".join(lines[start_line - 1 : end_line]).rstrip()
        normalized = " ".join(sentence_text.split())
        record = {
            "source": path.relative_to(WORK).as_posix(),
            "origin": origin,
            "module": sentence_module,
            "keyword": keyword,
            "start_line": start_line,
            "end_line": end_line,
            "attributes": attributes(sentence_text),
            "normalized_sha256": hashlib.sha256(normalized.encode()).hexdigest(),
            "text": sentence_text,
        }
        if origin == "candidate-proof" and keyword == "rule":
            assessment = PROOF_RULE_ASSESSMENTS.get(start_line)
            if assessment is None:
                record["extension_class"] = "UNMAPPED"
                record["assessment"] = "UNMAPPED proof-local rule"
            else:
                record["extension_class"] = assessment[0]
                record["assessment"] = assessment[1]
        elif origin == "trusted-supplied" and keyword == "rule":
            record["extension_class"] = "fixed-semantics"
            record["assessment"] = (
                "Trusted supplied operational/equational baseline. Reviewed "
                "for task-specific answer encoding and used-path fidelity; no "
                "candidate-local conclusion is introduced."
            )
        records.append(record)
    return records


def main() -> int:
    semantics_files = sorted((WORK / "reference-semantics").rglob("*.k"))
    proof_files = [WORK / "verification.k", WORK / "spec.k"]
    records = []
    for path in semantics_files:
        records.extend(scan_file(path, "trusted-supplied"))
    for path in proof_files:
        records.extend(scan_file(path, "candidate-proof"))

    by_keyword: dict[str, int] = {}
    by_origin: dict[str, int] = {}
    for record in records:
        by_keyword[record["keyword"]] = by_keyword.get(record["keyword"], 0) + 1
        by_origin[record["origin"]] = by_origin.get(record["origin"], 0) + 1

    function_declarations = [
        record
        for record in records
        if record["keyword"] == "syntax"
        and any(
            token == "function"
            or token == "total"
            or token.startswith("functional")
            for token in record["attributes"]
        )
    ]
    priority_rules = [
        record
        for record in records
        if record["keyword"] == "rule"
        and any(token.startswith("priority") for token in record["attributes"])
    ]
    simplification_rules = [
        record
        for record in records
        if record["keyword"] == "rule"
        and "simplification" in record["attributes"]
    ]
    candidate_rules = [
        record
        for record in records
        if record["origin"] == "candidate-proof" and record["keyword"] == "rule"
    ]
    unmapped_candidate_rules = [
        record for record in candidate_rules if record["assessment"].startswith("UNMAPPED")
    ]

    used_construct_map = {
        "Module/FuncDef/Params": [
            "reference-semantics/semantics/syntax.k:53-61",
            "reference-semantics/semantics/functions.k:14-16",
        ],
        "Assign/Name/Int/AugAssign": [
            "reference-semantics/semantics/syntax.k:9-13,41-45",
            "reference-semantics/semantics/core.k",
            "reference-semantics/semantics/operators.k",
        ],
        "For/#loop": [
            "reference-semantics/semantics/syntax.k:45",
            "reference-semantics/semantics/controls.k:58-79",
            "reference-semantics/semantics/iter.k",
        ],
        "Subscript/Slice/NoBound": [
            "reference-semantics/semantics/syntax.k:22,38-39",
            "reference-semantics/semantics/subscript.k",
        ],
        "If/Compare/CmpOp": [
            "reference-semantics/semantics/syntax.k:30-32,49",
            "reference-semantics/semantics/controls.k",
            "reference-semantics/semantics/operators.k",
        ],
        "Call/closureVal/return": [
            "reference-semantics/semantics/syntax.k:28,50",
            "reference-semantics/semantics/call.k",
            "reference-semantics/semantics/functions.k",
        ],
        "abs and integer addition/comparison": [
            "reference-semantics/semantics/builtins.k",
            "reference-semantics/semantics/operators.k",
            "reference-semantics/semantics/int.k",
            "verification.k:27-34",
        ],
        "list/vCons/ValSeq/valSeqConcat/vsLen/buildVS": [
            "reference-semantics/semantics/core.k",
            "reference-semantics/semantics/list.k",
            "reference-semantics/semantics/subscript.k",
            "verification.k:53-68",
        ],
        "scope maps and updates": [
            "reference-semantics/semantics.k configuration",
            "reference-semantics/semantics/core.k",
            "verification.k:39-49",
        ],
    }

    document = {
        "schema_version": 1,
        "semantics_files": [
            path.relative_to(WORK).as_posix() for path in semantics_files
        ],
        "proof_files": [path.relative_to(WORK).as_posix() for path in proof_files],
        "counts": {
            "sentences": len(records),
            "by_keyword": dict(sorted(by_keyword.items())),
            "by_origin": dict(sorted(by_origin.items())),
            "function_total_functional_declarations": len(function_declarations),
            "priority_rules": len(priority_rules),
            "simplification_rules": len(simplification_rules),
            "candidate_proof_rules": len(candidate_rules),
        },
        "used_construct_map": used_construct_map,
        "function_total_functional_declarations": function_declarations,
        "priority_rules": priority_rules,
        "simplification_rules": simplification_rules,
        "sentences": records,
    }
    json_path = EVIDENCE / "stage5-rule-inventory.json"
    json_path.write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    markdown = [
        "# Stage 5 exhaustive K sentence inventory",
        "",
        f"Total inventoried sentences: {len(records)}.",
        "",
        "| Origin | File | Module | Kind | Lines | Attributes | SHA-256 |",
        "|---|---|---|---|---:|---|---|",
    ]
    for record in records:
        attr_text = ", ".join(record["attributes"]).replace("|", "\\|")
        markdown.append(
            f"| {record['origin']} | `{record['source']}` | "
            f"`{record['module'] or '-'}` | {record['keyword']} | "
            f"{record['start_line']}-{record['end_line']} | {attr_text} | "
            f"`{record['normalized_sha256']}` |"
        )
    markdown.extend(
        [
            "",
            "## Candidate proof-local rule assessments",
            "",
            "| Lines | Class | Assessment |",
            "|---:|---|---|",
        ]
    )
    for record in candidate_rules:
        markdown.append(
            f"| {record['start_line']}-{record['end_line']} | "
            f"{record['extension_class']} | {record['assessment']} |"
        )
    markdown.extend(
        [
            "",
            "## Rule-by-rule dispositions",
            "",
            "| Origin | File | Lines | Class | Assessment |",
            "|---|---|---:|---|---|",
        ]
    )
    for record in records:
        if record["keyword"] != "rule":
            continue
        assessment = str(record.get("assessment", "")).replace("|", "\\|")
        extension_class = record.get("extension_class", "declaration")
        markdown.append(
            f"| {record['origin']} | `{record['source']}` | "
            f"{record['start_line']}-{record['end_line']} | "
            f"{extension_class} | {assessment} |"
        )
    markdown_path = EVIDENCE / "stage5-rule-inventory.md"
    markdown_path.write_text("\n".join(markdown) + "\n", encoding="utf-8")

    print(f"json_inventory={json_path}")
    print(f"json_sha256={hashlib.sha256(json_path.read_bytes()).hexdigest()}")
    print(f"markdown_inventory={markdown_path}")
    print(
        f"markdown_sha256={hashlib.sha256(markdown_path.read_bytes()).hexdigest()}"
    )
    print(f"sentence_count={len(records)}")
    print(f"by_keyword={dict(sorted(by_keyword.items()))}")
    print(f"by_origin={dict(sorted(by_origin.items()))}")
    print(f"function_total_functional_count={len(function_declarations)}")
    print(f"priority_rule_count={len(priority_rules)}")
    print(f"simplification_rule_count={len(simplification_rules)}")
    print(f"candidate_rule_count={len(candidate_rules)}")
    print(f"unmapped_candidate_rule_count={len(unmapped_candidate_rules)}")
    for record in candidate_rules:
        print(
            f"CANDIDATE_RULE lines={record['start_line']}-{record['end_line']} "
            f"class={record['extension_class']} sha256="
            f"{record['normalized_sha256']} assessment={record['assessment']}"
        )
    return 1 if unmapped_candidate_rules else 0


if __name__ == "__main__":
    sys.exit(main())
