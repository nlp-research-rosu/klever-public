#!/usr/bin/env python3
"""Create an exhaustive lexical inventory of all submitted/local K sentences.

The source files are small, consistently formatted K modules.  A local
sentence begins either at column zero (requires/module/endmodule) or with the
module's two-space indentation.  Continuation clauses are more deeply
indented, so this preserves every complete declaration/rule/claim span.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import re


ROOT = Path("/tmp/audit-work/reconstruction")
OUTPUT_JSON = Path("/audit-output/evidence/05-rule-inventory.json")
OUTPUT_MD = Path("/audit-output/evidence/05-rule-inventory.md")

START = re.compile(
    r"^(?:(?P<root>requires|module|endmodule)\b|"
    r"  (?P<inner>imports|syntax|rule|configuration|context|claim|alias)\b)"
)
ATTRIBUTE_TOKEN = re.compile(
    r"^(?:function|functional|total|macro|simplification|owise|concrete|"
    r"token|strict(?:\([^)]*\))?|seqstrict(?:\([^)]*\))?|"
    r"symbol(?:\([^)]*\))?|hook(?:\([^)]*\))?|priority(?:\([^)]*\))?)$"
)

MATERIAL_FIXED_MODULES = {
    "semantics.k",
    "syntax.k",
    "core.k",
    "iter.k",
    "operators.k",
    "int.k",
    "bool.k",
    "list.k",
    "controls.k",
    "functions.k",
    "call.k",
}


def sentences(path: Path) -> list[dict[str, object]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group("root") or match.group("inner")))
    records: list[dict[str, object]] = []
    for position, (start, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        body = "".join(lines[start:end]).rstrip()
        digest = hashlib.sha256(" ".join(body.split()).encode()).hexdigest()
        uncommented = "\n".join(
            line.split("//", 1)[0] for line in body.splitlines()
        )
        attributes: set[str] = set()
        for group in re.findall(r"\[([^\[\]]*)\]", uncommented):
            for token in group.split(","):
                normalized = token.strip()
                if ATTRIBUTE_TOKEN.fullmatch(normalized):
                    attributes.add(normalized)
        records.append(
            {
                "source": str(path),
                "relative_source": str(path.relative_to(ROOT)),
                "kind": kind,
                "start_line": start + 1,
                "end_line": start + body.count("\n") + 1,
                "sha256_normalized": digest,
                "attributes": sorted(attributes),
                "text": body,
            }
        )
    return records


def classify(record: dict[str, object]) -> tuple[str, str]:
    relative = str(record["relative_source"])
    line = int(record["start_line"])
    kind = str(record["kind"])
    base = Path(relative).name

    if relative.startswith("reference-semantics/"):
        if base == "concrete.k":
            return (
                "FIXED_SUPPLIED_CONCRETE_ONLY",
                "Trusted supplied semantics; imported only by MPY-KRUN, not by the proof definition.",
            )
        if base in MATERIAL_FIXED_MODULES:
            return (
                "FIXED_SUPPLIED_MATERIAL_MODULE",
                "Trusted supplied semantics; this module participates in parsing or the material execution path. Used constructs are mapped separately.",
            )
        return (
            "FIXED_SUPPLIED_UNUSED_MODULE",
            "Trusted supplied semantics; no constructor from this module is used by solution.mpy or the proof path.",
        )

    if relative == "verification.k":
        if kind in {"module", "endmodule", "imports", "requires"}:
            return ("STRUCTURE", "Module/import structure.")
        if line in (181,):
            return (
                "SOUND_DOMAIN_SYNTAX",
                "Unbounded recursive IntList domain; represents every finite integer sequence.",
            )
        if line in (183,):
            return (
                "INPUT_REPRESENTATION_SYMBOL",
                "Proof-side sequence representation. Its only material consumer is covered by the two structural iterator rules.",
            )
        if 186 <= line <= 190:
            return (
                "SOUND_INPUT_REPRESENTATION_RULE",
                "Constructor-complete iterator behavior for empty/cons IntList; no result oracle is introduced.",
            )
        if 194 <= line <= 248:
            if kind == "syntax" and line in (194, 208):
                return (
                    "LIMITED_TOTALITY_DECLARATION",
                    "Truthful and complete on the claim-reachable D>=2 domain; [total] is not globally covered at D=0 because pyMod(N,0) is undefined.",
                )
            return (
                "SOUND_DEFINITIONAL_SUMMARY",
                "Guarded recursive mathematical definition; guards partition every claim-reachable case and recursion descends/advances.",
            )
        if 251 <= line <= 302 or 341 <= line <= 343:
            return (
                "EXACT_MACRO",
                "AST constructor macro; the expanded solutionModule is mechanically identical to submitted solution.mpy.",
            )
        if 307 <= line <= 339:
            return (
                "OPERATIONAL_BRIDGE_EVIDENCE_GAP",
                "Exact bounded prefix for the immutable body by static composition, but no bridge-free universal K connection theorem is supplied.",
            )
        if 7 <= line <= 176:
            return (
                "SOUND_FIXED_RULE_SPECIALIZATION",
                "Guarded specialization or normalization of a supplied rule; same value/control/state update on its complete match domain.",
            )
        return (
            "REVIEWED_OTHER_LOCAL",
            "Local declaration reviewed; see Stage 5 narrative.",
        )

    if relative == "spec.k":
        if kind == "claim":
            return (
                "POSITIVE_REACHABILITY_CLAIM",
                "Reconstructed independently; dependency-ordered command exited 0 with #Top.",
            )
        return ("SPEC_STRUCTURE", "Specification module structure or imports.")

    return ("OTHER", "Not classified.")


def main() -> None:
    files = [ROOT / "reference-semantics" / "semantics.k"]
    files.extend(sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")))
    files.extend((ROOT / "verification.k", ROOT / "spec.k"))

    records: list[dict[str, object]] = []
    for path in files:
        for record in sentences(path):
            decision, rationale = classify(record)
            record["decision"] = decision
            record["rationale"] = rationale
            record["inventory_id"] = (
                f"{record['relative_source']}:{record['start_line']}:"
                f"{str(record['sha256_normalized'])[:12]}"
            )
            records.append(record)

    document = {
        "root": str(ROOT),
        "files": [str(path.relative_to(ROOT)) for path in files],
        "record_count": len(records),
        "kind_counts": Counter(str(record["kind"]) for record in records),
        "decision_counts": Counter(str(record["decision"]) for record in records),
        "records": records,
    }
    OUTPUT_JSON.write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    out: list[str] = [
        "# Exhaustive local K sentence inventory",
        "",
        f"Files: {len(files)}",
        f"Records: {len(records)}",
        "",
        "## Counts",
        "",
    ]
    for kind, count in sorted(document["kind_counts"].items()):
        out.append(f"- `{kind}`: {count}")
    out.extend(("", "## Review decisions", ""))
    for decision, count in sorted(document["decision_counts"].items()):
        out.append(f"- `{decision}`: {count}")
    out.extend(("", "## Records", ""))
    for record in records:
        attrs = ", ".join(f"`{a}`" for a in record["attributes"]) or "none"
        out.extend(
            (
                f"### {record['inventory_id']}",
                "",
                f"- Kind: `{record['kind']}`",
                f"- Lines: {record['start_line']}-{record['end_line']}",
                f"- Attributes: {attrs}",
                f"- Decision: `{record['decision']}`",
                f"- Rationale: {record['rationale']}",
                "",
                "```k",
                str(record["text"]),
                "```",
                "",
            )
        )
    OUTPUT_MD.write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {OUTPUT_JSON} and {OUTPUT_MD}")
    print(f"files={len(files)} records={len(records)}")
    print("kind_counts", dict(document["kind_counts"]))
    print("decision_counts", dict(document["decision_counts"]))


if __name__ == "__main__":
    main()
