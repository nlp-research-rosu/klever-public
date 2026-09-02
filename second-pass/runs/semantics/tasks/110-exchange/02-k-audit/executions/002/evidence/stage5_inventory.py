#!/usr/bin/env python3
import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/review")
FILES = [
    ROOT / "reference-semantics" / "semantics.k",
    *sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]

# Rules/contexts that can be exercised by the submitted program or are the
# fixed-semantics side of the intVals representation relation.
RELEVANT_FIXED = {
    "semantics/core.k": {
        125, 126, 127, 131, 132, 152, 158, 189, 190, 191, 194,
        200, 214, 215,
    },
    "semantics/call.k": {20, 21, 69},
    "semantics/functions.k": {14, 63, 64, 78, 85},
    "semantics/controls.k": {9, 20, 52, 53, 54, 69, 71, 72, 73},
    "semantics/operators.k": {15, 16, 12, 17},
    "semantics/int.k": {9, 15, 20, 23, 26, 27},
    "semantics/list.k": {9, 10},
    "semantics/tuple.k": {32},
    "semantics/str.k": {14, 15, 16},
}

START = re.compile(
    r"^\s*(module|endmodule|imports|configuration|context|syntax|rule|claim|priority)\b"
)
ATTRS = [
    "function",
    "functional",
    "total",
    "simplification",
    "concrete",
    "priority",
    "owise",
    "macro",
    "macro-rec",
    "symbol",
    "no-evaluators",
]


def display_path(path: Path) -> str:
    if path.name in {"verification.k", "spec.k"}:
        return path.name
    return path.relative_to(ROOT / "reference-semantics").as_posix()


entries = []
for path in FILES:
    lines = path.read_text().splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    for offset, (index, kind) in enumerate(starts):
        stop = starts[offset + 1][0] if offset + 1 < len(starts) else len(lines)
        block = "\n".join(lines[index:stop]).strip()
        single_line = " ".join(part.strip() for part in block.splitlines())
        code_only = "\n".join(part.split("//", 1)[0] for part in block.splitlines())
        bracket_text = " ".join(re.findall(r"\[([^\]]+)\]", code_only))
        attributes = ",".join(
            attribute
            for attribute in ATTRS
            if re.search(rf"(?<![\w-]){re.escape(attribute)}(?![\w-])", bracket_text)
        )
        relative = display_path(path)
        line_number = index + 1
        if relative == "verification.k":
            disposition = "PROOF_LOCAL_MANUAL_ACCEPT"
        elif relative == "spec.k":
            disposition = "CLAIM_MANUAL_REVIEW"
        elif line_number in RELEVANT_FIXED.get(relative, set()):
            disposition = "FIXED_RELEVANT_MANUAL_ACCEPT"
        else:
            disposition = "FIXED_UNUSED_NO_SUBMITTED_PROGRAM_PATH"
        entries.append(
            (
                relative,
                line_number,
                kind,
                attributes or "-",
                disposition,
                single_line,
            )
        )

counts = collections.Counter(entry[2] for entry in entries)
dispositions = collections.Counter(entry[4] for entry in entries)
rule_dispositions = collections.Counter(entry[4] for entry in entries if entry[2] == "rule")
attribute_counts = collections.Counter()
for entry in entries:
    for attribute in entry[3].split(","):
        if attribute != "-":
            attribute_counts[attribute] += 1

print("path\tline\tkind\tattributes\tdisposition\tdeclaration_or_rule")
for entry in entries:
    print("\t".join(map(str, entry)))
print("SUMMARY_KINDS", " ".join(f"{key}={counts[key]}" for key in sorted(counts)))
print(
    "SUMMARY_ATTRIBUTES",
    " ".join(f"{key}={attribute_counts[key]}" for key in sorted(attribute_counts)),
)
print(
    "SUMMARY_DISPOSITIONS",
    " ".join(f"{key}={dispositions[key]}" for key in sorted(dispositions)),
)
print(
    "SUMMARY_RULE_DISPOSITIONS",
    " ".join(f"{key}={rule_dispositions[key]}" for key in sorted(rule_dispositions)),
)
