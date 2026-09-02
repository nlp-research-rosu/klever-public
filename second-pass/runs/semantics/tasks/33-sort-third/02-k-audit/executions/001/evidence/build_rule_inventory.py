#!/usr/bin/env python3
"""Build a source-ordered inventory of all K declarations/rules under review."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


WORK = Path("/tmp/audit-work/audit-33-sort-third")
OUTPUT = Path("/audit-output/evidence/rule-inventory.json")
START = re.compile(
    r"^\s*(module|imports|syntax|configuration|context|rule|claim|endmodule)\b"
)


VERIFICATION_ASSESSMENTS = {
    1: "Imports only the byte-identical trusted supplied semantics entry point.",
    3: "Candidate proof-extension module boundary.",
    4: "Imports the fixed MPY semantics; no generated or alternate semantics module.",
    6: "Exact AST alias declaration for the real loop body; total nullary function.",
    7: "Exact expansion of the submitted loop body; no execution is bypassed.",
    23: "Exact AST alias declaration for the submitted function body.",
    24: "Exact expansion of the submitted function body, using the exact loop alias.",
    38: "Exact closure-value alias declaration.",
    39: "Matches fixed FuncDef closure construction: parameter l, body, defining scope 0.",
    44: "Exact submitted-module alias declaration.",
    45: "Reduces to the trusted-translator AST; independently checked by pinning.k.",
    55: "Mathematical per-position summary; two disjoint, exhaustive mod-3 branches.",
    56: "At indices divisible by 3, selects sorted slice position I/3; valid for divisor 3.",
    59: "At all other indices, preserves the iterated input value; guard disjoint from line 56.",
    62: "Structurally recursive loop-fold summary declaration.",
    64: "Truthful base case: no remaining input leaves the accumulated prefix unchanged.",
    65: "Truthful descending fold step; consumes one input and appends exactly one selected value.",
    75: "Structurally recursive final-loop-value declaration.",
    76: "Truthful empty-iteration case: preserves the old loop target value.",
    77: "Truthful nonempty case: recursively returns the last input element.",
    80: "End-to-end mathematical transformation summary declaration.",
    81: "Composes every-third slicing, trusted sortVS, and the truthful loop fold.",
    87: "Candidate proof-extension module boundary.",
}

SPEC_ASSESSMENTS = {
    9: (
        "Auxiliary circularity over the real #loop control point. It preserves arbitrary "
        "continuation and unrelated scope/heap map frames while constraining i, value, and result."
    ),
    39: (
        "Result-constraining entry reachability claim. It loads the exact module alias, executes "
        "the real call, returns ref(2), and fixes the resulting heap list to sortThird(INPUT)."
    ),
}


def source_files() -> list[Path]:
    return [
        WORK / "reference-semantics" / "semantics.k",
        *sorted((WORK / "reference-semantics" / "semantics").glob("*.k")),
        WORK / "verification.k",
        WORK / "spec.k",
    ]


def statements(path: Path) -> list[dict[str, object]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        if line.startswith("requires "):
            starts.append((index, "requires"))
            continue
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    records: list[dict[str, object]] = []
    for position, (start_index, keyword) in enumerate(starts):
        end_index = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block_lines = lines[start_index:end_index]
        while block_lines and (
            not block_lines[-1].strip()
            or block_lines[-1].lstrip().startswith("//")
        ):
            block_lines.pop()
        text = "\n".join(block_lines).strip()
        compact = re.sub(r"\s+", " ", text)
        flags = {
            "function": "[function" in text or ", function" in text,
            "total": bool(re.search(r"\btotal\b", text)),
            "functional": bool(re.search(r"\bfunctional\b", text)),
            "symbol": "symbol(" in text,
            "opaque_no_evaluators": "no-evaluators" in text,
            "priority": "priority(" in text,
            "simplification": "simplification" in text,
            "concrete_only": "[concrete]" in text,
            "owise": "[owise]" in text,
        }
        if keyword == "rule":
            subtype = "simplification_rule" if flags["simplification"] else "ordinary_rule"
        elif keyword == "syntax":
            subtype = "syntax_declaration"
        elif keyword == "context":
            subtype = "evaluation_context"
        else:
            subtype = keyword

        relative = str(path.relative_to(WORK))
        if relative.startswith("reference-semantics/"):
            assessment = (
                "Accepted as an unchanged declaration/rule of the trusted SUPPLIED_SEMANTICS "
                "baseline; candidate/reference recursive integrity matched. Used-path behavior "
                "and opaque primitives are assessed separately in REVIEW.md."
            )
            origin = "trusted_supplied_semantics"
        elif relative == "verification.k":
            assessment = VERIFICATION_ASSESSMENTS.get(
                start_index + 1,
                "Candidate verification entry requiring manual classification.",
            )
            origin = "candidate_proof_extension"
        else:
            assessment = SPEC_ASSESSMENTS.get(
                start_index + 1,
                "Candidate specification/module structure.",
            )
            origin = "candidate_specification"

        records.append(
            {
                "file": relative,
                "start_line": start_index + 1,
                "end_line": start_index + len(block_lines),
                "keyword": keyword,
                "subtype": subtype,
                "flags": flags,
                "origin": origin,
                "assessment": assessment,
                "source": compact,
            }
        )
    return records


def main() -> int:
    records = [record for path in source_files() for record in statements(path)]
    keyword_counts = Counter(str(record["keyword"]) for record in records)
    origin_counts = Counter(str(record["origin"]) for record in records)
    flag_counts = Counter(
        flag
        for record in records
        for flag, enabled in dict(record["flags"]).items()
        if enabled
    )
    unresolved = [
        record
        for record in records
        if "requiring manual classification" in str(record["assessment"])
    ]
    document = {
        "scope": [
            "reference-semantics/semantics.k",
            "reference-semantics/semantics/*.k",
            "verification.k",
            "spec.k",
        ],
        "record_count": len(records),
        "keyword_counts": dict(sorted(keyword_counts.items())),
        "origin_counts": dict(sorted(origin_counts.items())),
        "flag_counts": dict(sorted(flag_counts.items())),
        "unresolved_candidate_extension_count": len(unresolved),
        "records": records,
    }
    OUTPUT.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                key: document[key]
                for key in (
                    "scope",
                    "record_count",
                    "keyword_counts",
                    "origin_counts",
                    "flag_counts",
                    "unresolved_candidate_extension_count",
                )
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 1 if unresolved else 0


if __name__ == "__main__":
    raise SystemExit(main())
