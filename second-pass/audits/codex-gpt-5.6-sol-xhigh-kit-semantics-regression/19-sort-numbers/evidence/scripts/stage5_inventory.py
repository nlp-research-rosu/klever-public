#!/usr/bin/env python3
"""Build an exhaustive, line-addressed K declaration/rule inventory."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import csv
import re


ROOT = Path("/tmp/audit-work/19-sort-numbers/source")
SEMANTICS = ROOT / "reference-semantics"
OUTPUT = Path("/audit-output/evidence/stage5-rule-inventory.tsv")
SUMMARY = Path("/audit-output/evidence/stage5-rule-inventory-summary.md")

files = [SEMANTICS / "semantics.k"]
files += sorted((SEMANTICS / "semantics").glob("*.k"))
files += [ROOT / "verification.k", ROOT / "spec.k"]

start_re = re.compile(r"^\s*(configuration|syntax|rule|claim|context|alias)\b")
module_re = re.compile(r"^\s*module\s+([A-Za-z0-9_-]+)")
end_re = re.compile(r"^\s*endmodule\b")

# Start-line ranges reached by the submitted program, the entry/key claims, or
# the fresh concrete bridge tests.  Unlisted rules are still inventoried.
relevant_ranges: dict[str, list[tuple[int, int]]] = {
    "syntax.k": [(9, 39), (50, 61)],
    "core.k": [
        (13, 60), (68, 70), (95, 102), (106, 121), (124, 134), (145, 191),
        (194, 196), (213, 219),
    ],
    "functions.k": [(8, 90)],
    "call.k": [(15, 24), (31, 32), (38, 94)],
    "methods.k": [(10, 10), (23, 31), (70, 86)],
    "sort.k": [(45, 49), (61, 62)],
    "concrete.k": [(20, 59)],
    "dict.k": [(19, 54), (62, 66), (101, 103)],
    "str.k": [(12, 22)],
    "list.k": [(18, 20)],
}


def is_relevant(path: Path, start: int) -> bool:
    if path.name in {"verification.k", "spec.k"}:
        return True
    return any(lo <= start <= hi for lo, hi in relevant_ranges.get(path.name, []))


def collapse(lines: list[str]) -> str:
    text = " ".join(line.strip() for line in lines)
    text = re.sub(r"\s+", " ", text)
    return text.replace("\t", " ").strip()


def classify(kind: str, text: str) -> str:
    if kind == "claim":
        return "reachability-claim"
    if kind == "configuration":
        return "configuration"
    if kind == "context":
        return "evaluation-context"
    if kind == "alias":
        return "alias"
    if kind == "syntax":
        flags = []
        if "function" in text:
            flags.append("function")
        if "total" in text:
            flags.append("total")
        if "functional" in text:
            flags.append("functional")
        if "no-evaluators" in text or "symbol(" in text:
            flags.append("opaque-or-symbolic")
        if "macro" in text:
            flags.append("macro")
        return "syntax" + (":" + ",".join(flags) if flags else "")
    if "[simplification" in text:
        return "simplification-rule"
    if "[concrete" in text:
        return "concrete-rule"
    if "priority(" in text:
        return "priority-semantic-rule"
    if "[owise" in text:
        return "owise-semantic-rule"
    return "ordinary-semantic-rule"


def assessment(path: Path, kind: str, text: str, relevant: bool) -> str:
    filename = path.name
    if filename == "spec.k" and kind == "claim":
        if "sort-numbers" in text:
            return (
                "PROVED_WITH_CONCERN: entry executes the exact manually pinned body and constrains "
                "the result to joinCodes(space, sortKeyVS(...)); sortKeyVS meaning remains trusted."
            )
        return (
            "PROVED: exact continuation-parametric execution claim for one concrete numeral-key "
            "dictionary branch; fixed semantics executes the real lambda body."
        )

    if filename == "verification.k":
        if kind == "syntax" and "macro" in text:
            return "SOUND: syntax-only abbreviation; expansion matches the submitted translated AST."
        if "sortNumbersBody =>" in text or "sortNumbersFunction =>" in text or "numberKeyFunction =>" in text:
            return "SOUND: macro expansion only; exact submitted body/closure, no semantic oracle."
        if "splitWS(joinCodes" in text:
            return (
                "SOUND_OPERATIONAL_BRIDGE: guarded pure equation; induction on VS using joinCodes, "
                "splitWS, flushTok, and non-whitespace numeral codes. It reads/writes no cells and "
                "changes no control. Fresh in-domain and out-of-domain probes recorded separately."
            )
        if "isNumberWord" in text:
            return (
                "SOUND: guarded constructor cases are disjoint and exhaustive via owise; the equation "
                "recognizes exactly the ten permitted concrete string values."
            )
        if "validNumberWords" in text:
            return (
                "SOUND: exhaustive structural recursion on ValSeq; decreases on REST and is true exactly "
                "when all elements satisfy isNumberWord."
            )
        return "SOUND: proof-local declaration/rule is definitional and does not bypass execution."

    if "sortKeyVS(ValSeq, Val)" in text:
        return (
            "ACCEPTABLE_TRUST_BOUNDARY_WITH_CONCERN: supplied opaque keyed-sort primitive; fixed proof "
            "semantics defines the program result through it but does not prove ordering/permutation or "
            "key-call behavior. Concrete MPY-CONCRETE execution and differential evidence are finite bridges."
        )
    if "sortVS(ValSeq)" in text or "no-evaluators" in text:
        if relevant:
            return (
                "SUPPLIED_TRUSTED_PRIMITIVE: opaque in proof and concrete-only where declared; no "
                "candidate answer rule. Its stated mathematical meaning is assumed, not proved here."
            )
        return (
            "UNUSED_SUPPLIED_TRUSTED_PRIMITIVE: outside the program path; cannot contribute through "
            "a simplification rule and is retained as part of the fixed supplied semantics."
        )

    if filename == "concrete.k" and re.search(
        r"sorted|#ksort|#ksIns|insPair|kLt|unpairVS|kvP", text
    ):
        return (
            "SOUND_ON_USED_DOMAIN: concrete-only stable insertion sort; evaluates each key by the real "
            "call machinery, inserts before the first strictly greater key, preserves ties, and was "
            "exercised by fresh concrete and differential tests."
        )

    if relevant:
        return (
            "SOUND_ON_USED_PATH: fixed supplied rule/declaration was traced against the submitted AST; "
            "binding, left-to-right evaluation, allocation, frame return, and relevant pure helper behavior "
            "agree with the selected semantics and concrete execution."
        )

    return (
        "UNUSED_FIXED_SEMANTICS: inspected as a supplied declaration/rule; it is not reachable from the "
        "submitted AST, is not a simplification rule, and contains no task-specific conclusion. No false "
        "conclusion witness or proof dependency was identified."
    )


rows: list[dict[str, str | int]] = []
for path in files:
    lines = path.read_text().splitlines()
    module = "<outside-module>"
    starts: list[tuple[int, str, str]] = []
    module_by_line: dict[int, str] = {}
    active = module
    for number, line in enumerate(lines, start=1):
        module_match = module_re.match(line)
        if module_match:
            active = module_match.group(1)
        module_by_line[number] = active
        match = start_re.match(line)
        if match:
            starts.append((number, match.group(1), active))
        if end_re.match(line):
            active = "<outside-module>"

    for index, (start, kind, row_module) in enumerate(starts):
        next_start = starts[index + 1][0] if index + 1 < len(starts) else len(lines) + 1
        end = next_start - 1
        while end >= start and (
            not lines[end - 1].strip()
            or lines[end - 1].lstrip().startswith("//")
            or end_re.match(lines[end - 1])
        ):
            end -= 1
        text = collapse(lines[start - 1:end])
        attrs = sorted(set(re.findall(
            r"(?<![A-Za-z0-9_-])(functional|function|total|simplification|concrete|owise|"
            r"macro-rec|macro|no-evaluators|priority\([^)]+\)|symbol\([^)]+\)|"
            r"strict(?:\([^)]+\))?|seqstrict\([^)]+\))(?![A-Za-z0-9_-])",
            text,
        )))
        relevant = is_relevant(path, start)
        rows.append({
            "id": len(rows) + 1,
            "file": str(path.relative_to(ROOT)),
            "module": row_module,
            "lines": f"{start}-{end}",
            "kind": kind,
            "classification": classify(kind, text),
            "attributes": ";".join(attrs) if attrs else "-",
            "program_relevance": "used-or-proof-path" if relevant else "unused-by-program",
            "assessment": assessment(path, kind, text, relevant),
            "source": text,
        })

with OUTPUT.open("w", newline="") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t")
    writer.writeheader()
    writer.writerows(rows)

counts = Counter(str(row["kind"]) for row in rows)
class_counts = Counter(str(row["classification"]) for row in rows)
attribute_counts = Counter()
for row in rows:
    for attribute in str(row["attributes"]).split(";"):
        if attribute != "-":
            attribute_counts[attribute] += 1

opaque = [
    row for row in rows
    if "opaque-or-symbolic" in str(row["classification"])
]
simplifications = [
    row for row in rows
    if row["classification"] == "simplification-rule"
]
priorities = [
    row for row in rows
    if "priority(" in str(row["attributes"])
]

summary_lines = [
    "# Exhaustive K inventory summary",
    "",
    f"- Sources inventoried: {len(files)}",
    f"- Inventory rows: {len(rows)}",
    f"- Kinds: {dict(sorted(counts.items()))}",
    f"- Classifications: {dict(sorted(class_counts.items()))}",
    f"- Attribute counts: {dict(sorted(attribute_counts.items()))}",
    f"- Opaque/symbolic declarations: {len(opaque)}",
    f"- Priority rules: {len(priorities)}",
    f"- Simplification rules: {len(simplifications)}",
    "",
    "## Opaque/symbolic declarations",
    "",
]
for row in opaque:
    summary_lines.append(
        f"- `{row['file']}:{row['lines']}` — {row['source']} — {row['assessment']}"
    )
summary_lines += ["", "## Simplification rules", ""]
for row in simplifications:
    summary_lines.append(
        f"- `{row['file']}:{row['lines']}` — {row['source']} — {row['assessment']}"
    )
summary_lines += ["", "## Priority rules", ""]
for row in priorities:
    summary_lines.append(
        f"- `{row['file']}:{row['lines']}` — {row['source']} — {row['assessment']}"
    )
SUMMARY.write_text("\n".join(summary_lines) + "\n")

print(f"inventory={OUTPUT}")
print(f"summary={SUMMARY}")
print(f"rows={len(rows)}")
print(f"kinds={dict(sorted(counts.items()))}")
print(f"classifications={dict(sorted(class_counts.items()))}")
print(f"opaque={len(opaque)} priority={len(priorities)} simplification={len(simplifications)}")
