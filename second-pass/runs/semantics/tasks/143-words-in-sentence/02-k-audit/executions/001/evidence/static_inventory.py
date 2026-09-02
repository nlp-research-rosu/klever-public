#!/usr/bin/env python3
"""Create a line-addressed inventory of all local K declarations and rules."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


CANDIDATE = Path("/candidate")
OUTPUT_JSON = Path("/audit-output/evidence/static-inventory.json")
OUTPUT_MD = Path("/audit-output/evidence/static-inventory.md")
START = re.compile(r"^\s*(syntax|rule|claim|context|configuration|alias)\b")
BOUNDARY = re.compile(
    r"^\s*(syntax|rule|claim|context|configuration|alias|module|endmodule|imports)\b"
)


VERIFICATION_ASSESSMENTS = {
    9: "Sound free-algebra declaration for the proof's structural WordSeq induction.",
    15: "OPAQUE result-bearing ValSeq projection; no equations connect it to the fixed ValSeq constructors.",
    17: "UNJUSTIFIED operational iterator bridge for wordsVals; no bridge-free connection theorem.",
    20: "UNJUSTIFIED operational iterator bridge for wordsVals; no bridge-free connection theorem.",
    27: "OPAQUE result-bearing input-code projection; no equations connect it to concrete IntSeq codes.",
    29: "Sound structural sentence-length function on WordSeq.",
    30: "Sound empty-sequence length equation.",
    31: "Sound singleton-word length equation.",
    32: "Sound recursive word-and-separator length equation.",
    35: "Sound structural domain predicate declaration.",
    36: "Sound empty-sequence validity equation.",
    37: "Sound recursive nonempty/alphabetic-word validity equation.",
    43: "Total membership test matching prime lengths only on the theorem domain 1..100.",
    44: "Sound on lengths 1..100; deliberately false as a global primality characteristic above 100.",
    57: "Sound result-construction helper declaration.",
    58: "Sound empty-accumulator/prime-word selection case.",
    61: "Sound nonempty-accumulator/prime-word selection case.",
    65: "Sound nonprime-word rejection case; guards partition with the preceding two cases.",
    68: "Sound structural filter declaration.",
    69: "Sound filter base case.",
    70: "Sound recursive filter case.",
    74: "Exact source-expression macro; expanded-AST identity checked independently.",
    75: "Exact expansion of the submitted disjunction; expanded-AST identity checked independently.",
    104: "Exact loop-body macro declaration.",
    105: "Exact loop-body expansion; expanded-AST identity checked independently.",
    120: "Exact function-body macro declaration.",
    121: "Exact function-body expansion; expanded-AST identity checked independently.",
    133: "Exact submitted-program macro declaration.",
    134: "Exact submitted-program expansion; expanded-AST identity checked independently.",
    144: "UNJUSTIFIED result-bearing split bridge from opaque sentenceCodes to opaque wordsVals; no bridge-free universal connection theorem.",
    157: "Reachable-state-equivalent plain-frame target-binding shortcut; preserves all other cells and map entries.",
    178: "Reachable-state-equivalent assignment shortcut for existing integer n binding.",
    199: "Reachable-state-equivalent assignment shortcut for existing result binding.",
    220: "UNSOUND over its match domain: bypasses Name(\"len\") lookup and therefore ignores a shadowing local binding in M.",
    237: "Sound direct lookup shortcut because the explicit n entry is unique in the matched Map.",
    252: "Sound direct lookup shortcut because the explicit word entry is unique in the matched Map.",
    267: "Sound direct lookup shortcut because the explicit result entry is unique in the matched Map.",
}

SPEC_ASSESSMENTS = {
    8: "Result-constraining loop summary, but its arbitrary REST permits a shadowing len binding and it relies on the unsound len bridge.",
    48: "Result-constraining entry theorem under the extended theory; relies on the unconnected sentenceCodes/wordsVals operational abstraction.",
}


def extract(path: Path) -> list[dict[str, object]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    entries: list[dict[str, object]] = []
    index = 0
    while index < len(lines):
        match = START.match(lines[index])
        if match is None:
            index += 1
            continue
        kind = match.group(1)
        start = index
        index += 1
        while index < len(lines):
            if BOUNDARY.match(lines[index]):
                break
            index += 1
        end = index - 1
        while end > start and (
            not lines[end].strip() or lines[end].lstrip().startswith("//")
        ):
            end -= 1
        text = "\n".join(lines[start : end + 1])
        attribute_text = "\n".join(
            line.split("//", 1)[0] for line in lines[start : end + 1]
        )
        flags = []
        for flag in (
            "function",
            "total",
            "functional",
            "macro",
            "macro-rec",
            "simplification",
            "concrete",
            "priority",
            "owise",
            "anywhere",
            "symbol",
            "no-evaluators",
        ):
            if re.search(rf"\b{re.escape(flag)}\b", attribute_text):
                flags.append(flag)
        relative = str(path.relative_to(CANDIDATE))
        line = start + 1
        if relative.startswith("reference-semantics/"):
            assessment = (
                "Accepted at the selected SUPPLIED_SEMANTICS trust boundary: "
                "this entry is byte/type identical to the mounted trusted baseline. "
                "Task-used rules are mapped separately in REVIEW.md."
            )
        elif relative == "verification.k":
            assessment = VERIFICATION_ASSESSMENTS.get(
                line, "REVIEW GAP: verification entry lacks an explicit assessment."
            )
        elif relative == "spec.k":
            assessment = SPEC_ASSESSMENTS.get(
                line, "Specification declaration; scope described in REVIEW.md."
            )
        else:
            assessment = "Unclassified local entry."
        entries.append(
            {
                "file": relative,
                "start_line": line,
                "end_line": end + 1,
                "kind": kind,
                "flags": flags,
                "text": text,
                "assessment": assessment,
            }
        )
    return entries


def markdown_escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", "<br>")


def main() -> int:
    paths = sorted((CANDIDATE / "reference-semantics").rglob("*.k"))
    paths += [CANDIDATE / "verification.k", CANDIDATE / "spec.k"]
    entries = [entry for path in paths for entry in extract(path)]
    gaps = [
        entry
        for entry in entries
        if str(entry["assessment"]).startswith(("REVIEW GAP", "Unclassified"))
    ]
    counts = Counter(str(entry["kind"]) for entry in entries)
    payload = {
        "source_root": str(CANDIDATE),
        "files": [str(path.relative_to(CANDIDATE)) for path in paths],
        "entry_count": len(entries),
        "counts_by_kind": dict(sorted(counts.items())),
        "review_gap_count": len(gaps),
        "entries": entries,
    }
    OUTPUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Exhaustive K source inventory",
        "",
        f"Files: {len(paths)}; entries: {len(entries)}; explicit review gaps: {len(gaps)}.",
        "",
        "The supplied-semantics entries are accepted at the problem-selected trusted",
        "semantic boundary after byte/type identity checking. Candidate-local",
        "`verification.k` entries receive individual assessments below.",
        "",
        "| File:line | Kind / flags | Declaration or rule | Assessment |",
        "|---|---|---|---|",
    ]
    for entry in entries:
        location = f"{entry['file']}:{entry['start_line']}-{entry['end_line']}"
        kind_flags = str(entry["kind"])
        if entry["flags"]:
            kind_flags += " [" + ", ".join(entry["flags"]) + "]"
        normalized = " ".join(str(entry["text"]).split())
        lines.append(
            "| "
            + markdown_escape(location)
            + " | "
            + markdown_escape(kind_flags)
            + " | "
            + markdown_escape(normalized)
            + " | "
            + markdown_escape(str(entry["assessment"]))
            + " |"
        )
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"files={len(paths)}")
    print(f"entries={len(entries)}")
    print(f"counts_by_kind={json.dumps(dict(sorted(counts.items())))}")
    print(f"review_gap_count={len(gaps)}")
    print(f"json={OUTPUT_JSON}")
    print(f"markdown={OUTPUT_MD}")
    return 1 if gaps else 0


if __name__ == "__main__":
    raise SystemExit(main())
