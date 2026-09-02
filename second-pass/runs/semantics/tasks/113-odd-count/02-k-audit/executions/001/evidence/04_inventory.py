#!/usr/bin/env python3
"""Create a line-addressable exhaustive inventory of local K declarations.

This is intentionally lexical: each top-level declaration/rule/context/config
block is preserved verbatim (with whitespace normalized for TSV).  The audit
report supplies the semantic analysis and maps the submitted MPY constructs to
the relevant fixed-semantics entries.
"""

import csv
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/audit-113")
OUT = Path("/audit-output/evidence/04_rule_inventory.tsv")
SUMMARY = Path("/audit-output/evidence/04_rule_inventory_summary.txt")
KEYWORD = re.compile(
    r"^\s*(syntax|rule|context|configuration|claim|module|endmodule|imports)\b"
)


def blocks(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = KEYWORD.match(line)
        if match:
            starts.append((index, match.group(1)))
        elif line.startswith("requires "):
            starts.append((index, "requires"))
    for position, (start, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        parts = lines[start:end]
        text = " ".join(part.strip() for part in parts if part.strip())
        code = "\n".join(part.split("//", 1)[0] for part in parts)
        yield kind, start + 1, end, text, code


def disposition(source: str, line: int, kind: str, text: str):
    if source == "verification.k":
        if kind == "rule" and line == 28:
            return "EVIDENCE_GAP_RESULT_ABSTRACTION"
        if kind == "rule" and line == 132:
            return "REJECT_OVERBROAD_OPERATIONAL_BRIDGE"
        if kind == "rule" and line == 210:
            return "REJECT_SELF_JUSTIFYING_TASK_SUMMARY"
        if kind == "syntax" and "decimalCodes" in text:
            return "EVIDENCE_GAP_OPAQUE_RESULT_SYMBOL"
        if kind == "syntax" and "[macro]" in text:
            return "ACCEPT_PROGRAM_FRAGMENT_MACRO"
        if kind == "rule" and (
            "ODD-INNER-BODY" in text
            or "ODD-OUTER-BODY" in text
            or "ODD-COUNT-BODY" in text
            or "ODD-COUNT-PROGRAM" in text
        ):
            return "ACCEPT_BYTE_CHECKED_PROGRAM_RENDERING"
        if kind in {"rule", "syntax"}:
            return "ACCEPT_GUARDED_MATHEMATICAL_HELPER"
        return "STRUCTURAL"

    filename = Path(source).name
    used_modules = {
        "semantics.k",
        "syntax.k",
        "core.k",
        "iter.k",
        "operators.k",
        "int.k",
        "str.k",
        "list.k",
        "methods.k",
        "controls.k",
        "functions.k",
        "builtins.k",
        "call.k",
    }
    if filename in used_modules:
        return "SUPPLIED_FIXED_SEMANTICS_REVIEWED_USED_MODULE"
    return "SUPPLIED_FIXED_SEMANTICS_NOT_REACHED_BY_PROGRAM"


def main():
    sources = [ROOT / "reference-semantics" / "semantics.k"]
    sources.extend(sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")))
    sources.append(ROOT / "verification.k")

    rows = []
    for path in sources:
        if path == ROOT / "verification.k":
            source = "verification.k"
            origin = "candidate-proof-extension"
        else:
            source = str(path.relative_to(ROOT / "reference-semantics"))
            origin = "trusted-supplied-fixed-semantics"
        for kind, start, end, text, code in blocks(path):
            attrs = []
            for attr in (
                "function",
                "total",
                "functional",
                "no-evaluators",
                "simplification",
                "priority",
                "owise",
                "concrete",
                "macro",
                "strict",
                "seqstrict",
            ):
                if re.search(rf"\b{re.escape(attr)}\b", code):
                    attrs.append(attr)
            rows.append(
                {
                    "origin": origin,
                    "source": source,
                    "kind": kind,
                    "start_line": start,
                    "end_line": end,
                    "attributes": ",".join(attrs) or "-",
                    "disposition": disposition(source, start, kind, text),
                    "text": text.replace("\t", " "),
                }
            )

    with OUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=[
                "origin",
                "source",
                "kind",
                "start_line",
                "end_line",
                "attributes",
                "disposition",
                "text",
            ],
            dialect="excel-tab",
        )
        writer.writeheader()
        writer.writerows(rows)

    counts = {}
    dispositions = {}
    for row in rows:
        counts[row["kind"]] = counts.get(row["kind"], 0) + 1
        dispositions[row["disposition"]] = dispositions.get(row["disposition"], 0) + 1
    lines = [
        f"source_count={len(sources)}",
        f"inventory_entry_count={len(rows)}",
        "kind_counts=" + ",".join(f"{key}:{counts[key]}" for key in sorted(counts)),
        "disposition_counts="
        + ",".join(f"{key}:{dispositions[key]}" for key in sorted(dispositions)),
        f"inventory_path={OUT}",
    ]
    SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
