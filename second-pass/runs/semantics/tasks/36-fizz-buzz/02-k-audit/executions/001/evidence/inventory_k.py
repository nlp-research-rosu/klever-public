#!/usr/bin/env python3
"""Produce an exhaustive declaration/rule/claim ledger for the audited K sources."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path


START = re.compile(r"^\s*(syntax|rule|context|configuration|claim)\b")
END = re.compile(r"^\s*endmodule\b")
ATTR = re.compile(r"\[([^\]]+)\]")


def blocks(path: Path):
    lines = path.read_text().splitlines()
    starts = [i for i, line in enumerate(lines) if START.match(line)]
    for pos, start in enumerate(starts):
        end = starts[pos + 1] if pos + 1 < len(starts) else len(lines)
        for j in range(start + 1, end):
            if END.match(lines[j]):
                end = j
                break
        body = lines[start:end]
        while len(body) > 1 and (
            not body[-1].strip() or body[-1].lstrip().startswith("//")
        ):
            body.pop()
        text = "\n".join(body).strip()
        kind = START.match(lines[start]).group(1)  # type: ignore[union-attr]
        yield start + 1, kind, text


def classification(path: Path, kind: str, text: str) -> tuple[str, str, str]:
    if "reference-semantics" in path.parts:
        source = "trusted-supplied-semantics"
        if kind == "rule":
            decision = "ACCEPTED_TRUSTED_BASELINE"
        else:
            decision = "DECLARATION_TRUSTED_BASELINE"
        relevance = "see-review-used-construct-map"
        return source, decision, relevance

    if path.name == "verification.k":
        source = "candidate-proof-extension"
        if "fizzBuzzAcc" in text or "fizzBuzzSpec" in text:
            return source, "SOUND_MATH_BUT_UNUSED_BY_ENTRY_CLAIMS", "unused"
        if "divisibleBy11Or13" in text:
            return source, "SOUND_MATH_BUT_UNUSED_BY_ENTRY_CLAIMS", "unused"
        if "countSevensAcc" in text:
            return source, "SOUND_ON_GUARDED_NONNEGATIVE_DOMAIN", "inner-claim"
        if "FIZZ-BUZZ-DEF" in text:
            return source, "EXACT_AST_MACRO_BUT_UNUSED", "unused"
        if "INNER-BODY" in text or "OUTER-BODY" in text or "FIZZ-BUZZ-CLOSURE" in text:
            return (
                source,
                "TRUTHFUL_AST_MACRO_BUT_NOT_LINKED_TO_SOLUTION_MPY",
                "substituted-entry-path",
            )
        return source, "REVIEWED_NO_FALSE_RULE_WITNESS", "other"

    return "candidate-specification", "CLAIM_REVIEWED_SEPARATELY", "claim"


def main() -> int:
    root = Path("/tmp/audit-work/fizz-buzz-audit")
    paths = sorted((root / "reference-semantics").rglob("*.k"))
    paths += [root / "verification.k", root / "spec-original.k"]
    writer = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    writer.writerow(
        (
            "id",
            "file",
            "line",
            "kind",
            "rule_class",
            "attributes",
            "source_class",
            "audit_decision",
            "path_relevance",
            "normalized_text",
        )
    )
    counts: dict[str, int] = {}
    item_id = 0
    for path in paths:
        for line, kind, text in blocks(path):
            item_id += 1
            counts[kind] = counts.get(kind, 0) + 1
            known_attrs = (
                "function",
                "total",
                "functional",
                "simplification",
                "concrete",
                "owise",
                "macro",
                "macro-rec",
                "no-evaluators",
                "bracket",
                "token",
            )
            attrs_found: list[str] = []
            for match in ATTR.findall(text):
                for part in match.split(","):
                    part = part.strip()
                    if (
                        part in known_attrs
                        or part.startswith("priority(")
                        or part.startswith("symbol(")
                        or part.startswith("strict")
                        or part.startswith("seqstrict")
                    ):
                        attrs_found.append(part)
            attrs = ",".join(attrs_found)
            if kind != "rule":
                rule_class = "n/a"
            elif "[simplification]" in text:
                rule_class = "simplification"
            elif "[macro" in text or "[macro-rec" in text:
                rule_class = "macro-equation"
            elif "<k>" in text:
                rule_class = "operational"
            else:
                rule_class = "equational"
            source, decision, relevance = classification(path, kind, text)
            writer.writerow(
                (
                    item_id,
                    str(path.relative_to(root)),
                    line,
                    kind,
                    rule_class,
                    attrs,
                    source,
                    decision,
                    relevance,
                    " ".join(text.split()),
                )
            )
    print(
        "# COUNTS "
        + " ".join(f"{key}={counts[key]}" for key in sorted(counts))
        + f" total={item_id}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
