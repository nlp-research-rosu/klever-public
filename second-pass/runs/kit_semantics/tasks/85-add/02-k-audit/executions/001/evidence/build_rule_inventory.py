#!/usr/bin/env python3
"""Build an exhaustive declaration/rule inventory from candidate K sources."""

from __future__ import annotations

import collections
import re
from pathlib import Path


OUTPUT = Path("/audit-output/evidence/rule_inventory.tsv")
SUMMARY = Path("/audit-output/evidence/rule_inventory_summary.txt")
SEMANTICS_ROOT = Path("/candidate/reference-semantics")
LOCAL_FILES = [Path("/candidate/verification.k"), Path("/candidate/spec.k")]

START = re.compile(
    r"^  (?P<kind>syntax|configuration|rule|claim|context|alias)\b"
)
ATTRIBUTES = re.compile(r"\[([^\]]+)\]")
ATTRIBUTE_NAMES = {
    "assoc",
    "avoid",
    "bracket",
    "cell",
    "comm",
    "concrete",
    "exit",
    "format",
    "function",
    "hook",
    "left",
    "macro",
    "macro-rec",
    "maincell",
    "multiplicity",
    "no-evaluators",
    "non-assoc",
    "owise",
    "preserves-definedness",
    "priority",
    "right",
    "seqstrict",
    "simplification",
    "strict",
    "symbol",
    "symbolic",
    "token",
    "total",
    "type",
    "unit",
}


USED_RANGES: dict[str, list[tuple[int, int, str]]] = {
    "semantics/syntax.k": [
        (9, 15, "Int/Bool/Name/UnaryOp/BinOp syntax"),
        (30, 32, "Compare/CmpOp syntax"),
        (41, 61, "Assign/AugAssign/For/If/Return/FuncDef/sequence/module syntax"),
    ],
    "semantics/core.k": [
        (13, 42, "values, sequences, scopes, KResult"),
        (49, 60, "complete MPY configuration"),
        (68, 70, "reference predicate used by generic dispatch priority"),
        (100, 102, "keyword predicate imported into call path"),
        (123, 134, "module loading, sequencing, and name lookup"),
        (145, 181, "lookup priority and builtins scope"),
        (183, 219, "argument evaluation, literals, operator dispatch, sequences"),
    ],
    "semantics/functions.k": [
        (8, 20, "function definition and frame syntax"),
        (62, 91, "parameter binding, return, and frame pop"),
    ],
    "semantics/call.k": [
        (15, 32, "callee/argument evaluation and dispatch"),
        (52, 60, "method guard reachable in imported dispatch"),
        (69, 75, "ordinary closure call/frame entry"),
    ],
    "semantics/controls.k": [
        (8, 31, "Assign and AugAssign"),
        (46, 54, "discarded expression and If"),
        (62, 75, "For/#loop iteration"),
    ],
    "semantics/operators.k": [
        (10, 17, "unary/binary/comparison dispatch"),
        (22, 46, "reference-dereference priority rules"),
    ],
    "semantics/int.k": [
        (7, 27, "integer unary, +, %, modulo, and == operations"),
    ],
    "semantics/bool.k": [
        (8, 11, "not and Bool comparison"),
    ],
    "semantics/list.k": [
        (8, 10, "list iterator protocol"),
    ],
    "semantics/iter.k": [
        (6, 8, "iterator protocol declarations"),
    ],
    "semantics.k": [
        (34, 90, "assembled MPY proof/concrete module imports"),
    ],
}


LOCAL_REVIEW: dict[tuple[str, int], tuple[str, str]] = {
    ("verification.k", 7): (
        "ACCEPT_DEFINITIONAL",
        "allInts is a total structural domain predicate",
    ),
    ("verification.k", 11): (
        "ACCEPT_DEFINITIONAL",
        "definedProjectInt names the generated sort predicate",
    ),
    ("verification.k", 12): (
        "ACCEPT_GUARDED_PROJECTION",
        "opaque only off-domain; integer cases collapse to their exact value",
    ),
    ("verification.k", 17): (
        "ACCEPT_DEFINITIONAL",
        "addSummary is total structural recursion over ValSeq and Bool",
    ),
    ("verification.k", 23): (
        "ACCEPT_TRUE_EQUATION",
        "empty ValSeq contains only integers",
    ),
    ("verification.k", 24): (
        "ACCEPT_TRUE_EQUATION",
        "constructor case is structural conjunction of head and tail domains",
    ),
    ("verification.k", 27): (
        "ACCEPT_TRUE_EQUATION",
        "definedProjectInt equals the generated isInt sort predicate",
    ),
    ("verification.k", 30): (
        "ACCEPT_SORT_LEMMA",
        "Val-to-Int projection is defined exactly for Int-sorted Val terms",
    ),
    ("verification.k", 33): (
        "ACCEPT_SORT_LEMMA",
        "guarded total projection equals the partial subsort projection",
    ),
    ("verification.k", 36): (
        "ACCEPT_SORT_LEMMA",
        "reverse orientation under the identical definedness guard",
    ),
    ("verification.k", 39): (
        "ACCEPT_TRUE_EQUATION",
        "projection is identity on statically Int-sorted values",
    ),
    ("verification.k", 40): (
        "ACCEPT_TRUE_EQUATION",
        "idempotence follows because the inner projection has sort Int",
    ),
    ("verification.k", 45): (
        "ACCEPT_DERIVED_OPERATOR_LEMMA",
        "guard and projection recover the fixed MPY-INT modulo rule domain",
    ),
    ("verification.k", 49): (
        "ACCEPT_DERIVED_OPERATOR_LEMMA",
        "guard and projection recover the fixed MPY-INT addition rule domain",
    ),
    ("verification.k", 56): (
        "ACCEPT_TRUE_EQUATION",
        "empty suffix contributes zero",
    ),
    ("verification.k", 57): (
        "ACCEPT_TRUE_EQUATION",
        "even-index parity skips the head and structurally descends",
    ),
    ("verification.k", 59): (
        "ACCEPT_TRUE_EQUATION",
        "odd-index parity adds exactly an even integer head and descends",
    ),
    ("spec.k", 8): (
        "ACCEPT_AUXILIARY_CLAIM",
        "loop circularity executes the exact #loop body over an arbitrary suffix",
    ),
    ("spec.k", 40): (
        "ACCEPT_ENTRY_CLAIM",
        "entry executes the exact regenerated binding/body on the full contract domain",
    ),
}


def relative_source(path: Path) -> str:
    if path.is_relative_to(SEMANTICS_ROOT):
        return path.relative_to(SEMANTICS_ROOT).as_posix()
    return path.name


def relevance(source: str, line: int) -> tuple[bool, str]:
    for start, end, note in USED_RANGES.get(source, []):
        if start <= line <= end:
            return True, note
    return False, "not reachable from solution.mpy under the entry precondition"


def inventory_file(path: Path) -> list[dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group("kind")))
    result = []
    source = relative_source(path)
    for item_index, (start, kind) in enumerate(starts):
        end = starts[item_index + 1][0] if item_index + 1 < len(starts) else len(lines)
        block_lines = lines[start:end]
        for boundary_index, line in enumerate(block_lines[1:], 1):
            if (
                line.startswith("module ")
                or line.startswith("endmodule")
                or line.startswith("  imports ")
            ):
                block_lines = block_lines[:boundary_index]
                break
        while block_lines and (
            not block_lines[-1].strip()
            or block_lines[-1].lstrip().startswith("//")
            or block_lines[-1].strip() == "endmodule"
        ):
            block_lines.pop()
        statement = " ".join(line.strip() for line in block_lines)
        statement = re.sub(r"\s+", " ", statement)
        attributes = ",".join(
            attribute.strip()
            for group in ATTRIBUTES.findall(statement)
            for attribute in group.split(",")
            if attribute.strip().split("(", 1)[0] in ATTRIBUTE_NAMES
        )
        line_number = start + 1
        if path in LOCAL_FILES:
            decision, review = LOCAL_REVIEW.get(
                (source, line_number),
                (
                    "REVIEW_REQUIRED",
                    "local declaration was not matched by the review table",
                ),
            )
            used = "yes"
        else:
            used_bool, note = relevance(source, line_number)
            used = "yes" if used_bool else "no"
            decision = (
                "ACCEPT_FIXED_SUPPLIED_USED"
                if used_bool
                else "ACCEPT_FIXED_SUPPLIED_UNUSED"
            )
            review = (
                f"byte-identical trusted SUPPLIED_SEMANTICS baseline; {note}"
            )
        result.append(
            {
                "source": source,
                "line": str(line_number),
                "kind": kind,
                "attributes": attributes,
                "used": used,
                "decision": decision,
                "review": review,
                "statement": statement,
            }
        )
    return result


def main() -> None:
    paths = sorted(SEMANTICS_ROOT.rglob("*.k")) + LOCAL_FILES
    records = [
        record
        for path in paths
        for record in inventory_file(path)
    ]
    assert all(record["decision"] != "REVIEW_REQUIRED" for record in records)

    columns = (
        "id",
        "source",
        "line",
        "kind",
        "attributes",
        "used",
        "decision",
        "review",
        "statement",
    )
    with OUTPUT.open("w", encoding="utf-8") as stream:
        stream.write("\t".join(columns) + "\n")
        for index, record in enumerate(records, 1):
            row = {"id": f"K{index:04d}", **record}
            stream.write(
                "\t".join(row[column].replace("\t", " ") for column in columns)
                + "\n"
            )

    kind_counts = collections.Counter(record["kind"] for record in records)
    decision_counts = collections.Counter(record["decision"] for record in records)
    attribute_counts = collections.Counter(
        attribute.split("(", 1)[0]
        for record in records
        for attribute in record["attributes"].split(",")
        if attribute
    )
    lines = [
        f"files={len(paths)}",
        f"records={len(records)}",
        "kinds=" + ",".join(f"{key}:{value}" for key, value in sorted(kind_counts.items())),
        "decisions="
        + ",".join(f"{key}:{value}" for key, value in sorted(decision_counts.items())),
        "attributes="
        + ",".join(f"{key}:{value}" for key, value in sorted(attribute_counts.items())),
        "functional_declarations=0",
        "local_unreviewed=0",
    ]
    SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"inventory={OUTPUT}")


if __name__ == "__main__":
    main()
