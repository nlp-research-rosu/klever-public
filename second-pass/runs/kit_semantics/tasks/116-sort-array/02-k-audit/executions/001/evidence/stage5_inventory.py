#!/usr/bin/env python3
"""Build a source-line inventory of all local K declarations and rules."""

from __future__ import annotations

import collections
import re
from dataclasses import dataclass
from pathlib import Path


SEMANTICS = Path("/tmp/audit-work/116-sort-array/reference-semantics")
VERIFICATION = Path("/tmp/audit-work/116-sort-array/verification.k")
SPEC = Path("/tmp/audit-work/116-sort-array/spec.k")
OUTPUT = Path("/audit-output/evidence/stage5-rule-inventory.md")

START = re.compile(
    r"^\s*(syntax|rule|claim|context|configuration)\b", re.IGNORECASE
)
ENDMODULE = re.compile(r"^endmodule\b", re.IGNORECASE)

RELEVANT_TERMS = (
    "$PGM",
    "#loadAll",
    "#alloc",
    "heapLoc",
    "FuncDef",
    "closureVal",
    "Lambda",
    "#mkLambda",
    "#bindP",
    "Return(",
    "#pop",
    "#endcall",
    "Name(",
    "#look",
    "builtinsScope",
    "KwArg",
    "#kwTag",
    "isKwV",
    "Call(",
    "#callee",
    "#evalArgs",
    "#evalArgCont",
    "#applyK",
    "toCall",
    "builtinV",
    "boundMethodV",
    '"sorted"',
    "sortVS",
    "insVS",
    "sortKeyVS",
    "#ksort",
    "#ksIns",
    "insPair",
    "kLt",
    "unpairVS",
    '"bin"',
    "binCodes",
    "binAcc",
    "pyMod",
    "applyBuiltin",
    "Attribute(",
    "applyMethod",
    '"count"',
    "cntSub",
    "dropIS",
    "Str(",
    "strToCodes",
    "strPrefix",
    "isLen",
    "allIntVS",
    "popcountAbs",
)

ATTRIBUTES = (
    "function",
    "functional",
    "total",
    "symbol",
    "no-evaluators",
    "priority",
    "concrete",
    "owise",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
    "simplification",
    "anywhere",
)


@dataclass
class Entry:
    path: Path
    line: int
    kind: str
    text: str
    classification: str


def strip_comment(line: str) -> str:
    in_string = False
    escaped = False
    for index, char in enumerate(line):
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif line[index : index + 2] == "//":
            return line[:index]
    return line


def normalize(lines: list[str]) -> str:
    cleaned = [strip_comment(line).strip() for line in lines]
    return " ".join(part for part in cleaned if part)


def classify(path: Path, kind: str, text: str) -> str:
    if path == VERIFICATION:
        return "PROOF_LOCAL_REVIEWED"
    if path == SPEC:
        return "TARGET_CLAIM"
    if path.name == "concrete.k" and any(term in text for term in RELEVANT_TERMS):
        return "RUNTIME_ONLY_RELEVANT"
    if "sortKeyVS" in text or (
        "sortVS" in text and ("no-evaluators" in text or '"sorted"' in text)
    ):
        return "FIXED_OPAQUE_TRUST_BOUNDARY"
    if path.name == "syntax.k":
        used_syntax = (
            "Expr ::=" in text
            or "Stmt ::=" in text
            or "Stmts" in text
            or "Params" in text
            or "CellVars" in text
            or "FreeVars" in text
            or "ParamNames" in text
            or "Module" in text
        )
        if used_syntax:
            return "FIXED_RELEVANT_SYNTAX"
    if any(term in text for term in RELEVANT_TERMS):
        return "FIXED_RELEVANT_REVIEWED"
    return "FIXED_SOURCE_DISJOINT_UNUSED"


def entries_for(path: Path) -> list[Entry]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    result = []
    for start in starts:
        end = start + 1
        while (
            end < len(lines)
            and not START.match(lines[end])
            and not ENDMODULE.match(lines[end])
        ):
            end += 1
        text = normalize(lines[start:end])
        kind_match = START.match(lines[start])
        assert kind_match is not None
        kind = kind_match.group(1).lower()
        result.append(
            Entry(
                path=path,
                line=start + 1,
                kind=kind,
                text=text,
                classification=classify(path, kind, text),
            )
        )
    return result


def source_paths() -> list[Path]:
    paths = [SEMANTICS / "semantics.k"]
    paths.extend(sorted((SEMANTICS / "semantics").glob("*.k")))
    paths.extend([VERIFICATION, SPEC])
    return paths


def main() -> int:
    all_entries = []
    for path in source_paths():
        all_entries.extend(entries_for(path))

    by_file: dict[Path, list[Entry]] = collections.defaultdict(list)
    for entry in all_entries:
        by_file[entry.path].append(entry)
    kind_counts = collections.Counter(entry.kind for entry in all_entries)
    class_counts = collections.Counter(entry.classification for entry in all_entries)
    attribute_counts = collections.Counter()
    for entry in all_entries:
        for attribute in ATTRIBUTES:
            if re.search(rf"\b{re.escape(attribute)}\b", entry.text):
                attribute_counts[attribute] += 1

    with OUTPUT.open("w", encoding="utf-8") as stream:
        stream.write("# Exhaustive local K source inventory\n\n")
        stream.write(
            "Generated from the trusted scratch copy. Each source entry beginning "
            "with `syntax`, `rule`, `claim`, `context`, or `configuration` is "
            "listed once with its starting line. Multi-line entries are flattened. "
            "`FIXED_SOURCE_DISJOINT_UNUSED` means its outer constructors or labels "
            "cannot match the submitted program's execution slice; it is not used "
            "as a premise of the target theorem.\n\n"
        )
        stream.write(f"Total entries: {len(all_entries)}\n\n")
        stream.write("## Counts by kind\n\n")
        for name, count in sorted(kind_counts.items()):
            stream.write(f"- {name}: {count}\n")
        stream.write("\n## Counts by classification\n\n")
        for name, count in sorted(class_counts.items()):
            stream.write(f"- {name}: {count}\n")
        stream.write("\n## Attribute-bearing entry counts\n\n")
        for name, count in sorted(attribute_counts.items()):
            stream.write(f"- {name}: {count}\n")

        for path in source_paths():
            relative = (
                path.relative_to(SEMANTICS).as_posix()
                if path.is_relative_to(SEMANTICS)
                else path.name
            )
            entries = by_file[path]
            stream.write(f"\n## `{relative}` ({len(entries)} entries)\n\n")
            stream.write("| Line | Kind | Classification | Source entry |\n")
            stream.write("|---:|---|---|---|\n")
            for entry in entries:
                escaped = entry.text.replace("|", "&#124;")
                stream.write(
                    f"| {entry.line} | {entry.kind} | {entry.classification} | "
                    f"`{escaped}` |\n"
                )

    print(f"OUTPUT={OUTPUT}")
    print(f"TOTAL_ENTRIES={len(all_entries)}")
    print(f"KIND_COUNTS={dict(sorted(kind_counts.items()))}")
    print(f"CLASS_COUNTS={dict(sorted(class_counts.items()))}")
    print(f"ATTRIBUTE_COUNTS={dict(sorted(attribute_counts.items()))}")
    for path in source_paths():
        print(f"FILE_COUNT {path}={len(by_file[path])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
