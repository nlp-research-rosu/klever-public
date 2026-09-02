#!/usr/bin/env python3
"""Build the exhaustive K sentence inventory used by the static audit."""

from __future__ import annotations

import hashlib
import re
import sys
from collections import Counter
from pathlib import Path


SEMANTICS = Path("/reference/reference-semantics")
CANDIDATE = Path("/candidate")
OUTPUT = Path(sys.argv[1])

paths = [SEMANTICS / "semantics.k", *sorted((SEMANTICS / "semantics").glob("*.k"))]
paths += [CANDIDATE / "verification.k", CANDIDATE / "spec.k"]

start_re = re.compile(r"^\s{2}(configuration|syntax|rule|claim|context)\b")
# A K attribute list is at the end of its source line (claim labels allow a
# trailing colon). This deliberately excludes Map lookup/update brackets and
# bracketed words in comments.
attribute_line_re = re.compile(
    r"\[("
    r"[A-Za-z][A-Za-z0-9-]*(?:\([^][]*\))?"
    r"(?:\s*,\s*[A-Za-z][A-Za-z0-9-]*(?:\([^][]*\))?)*"
    r")\]\s*:?\s*$"
)
attribute_name_re = re.compile(r"(?:^|,)\s*([A-Za-z][A-Za-z0-9-]*)")

# Source sentences reached by the exact submitted term or its two claims.
used: dict[str, set[int]] = {
    "semantics/syntax.k": {9, 32, 37, 41, 56, 57, 60, 61},
    "semantics/core.k": {
        13,
        15,
        18,
        25,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        49,
        124,
        125,
        126,
        127,
        130,
        131,
        132,
        152,
        157,
        158,
        185,
        186,
        189,
        190,
        191,
        194,
        195,
        199,
        200,
        208,
        209,
        210,
        213,
        214,
        215,
        227,
        228,
        229,
    },
    "semantics/iter.k": {8},
    "semantics/operators.k": {10, 12, 15, 16, 17},
    "semantics/int.k": {7, 9, 22, 25, 26},
    "semantics/bool.k": {16, 17, 18, 20, 22, 24},
    "semantics/str.k": {8, 9, 13, 14, 15},
    "semantics/tuple.k": {31, 32},
    "semantics/controls.k": {
        9,
        51,
        52,
        53,
        54,
        65,
        69,
        71,
        72,
        73,
        85,
    },
    "semantics/functions.k": {8, 14, 63, 64, 78, 80, 85},
    "semantics/builtins.k": {17, 143},
    "semantics/call.k": {19, 20, 21, 31, 69},
}


def relative(path: Path) -> str:
    if path.is_relative_to(SEMANTICS):
        return path.relative_to(SEMANTICS).as_posix()
    return path.name


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strip_line_comment(line: str) -> str:
    """Remove K // comments without treating // inside a string as a comment."""
    quoted = False
    escaped = False
    index = 0
    while index < len(line):
        char = line[index]
        if escaped:
            escaped = False
        elif char == "\\" and quoted:
            escaped = True
        elif char == '"':
            quoted = not quoted
        elif not quoted and line[index : index + 2] == "//":
            return line[:index]
        index += 1
    return line


def sentences(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [
        (index + 1, match.group(1))
        for index, line in enumerate(lines)
        if (match := start_re.match(line))
    ]
    for position, (line_number, kind) in enumerate(starts):
        end = starts[position + 1][0] - 1 if position + 1 < len(starts) else len(lines)
        for index in range(line_number, end + 1):
            if lines[index - 1].strip() == "endmodule":
                end = index - 1
                break
        block = "\n".join(lines[line_number - 1 : end]).rstrip()
        yield line_number, kind, block


all_sentences: list[tuple[str, int, str, str, list[str], str]] = []
attribute_counts: Counter[str] = Counter()
kind_counts: Counter[str] = Counter()
opaque: list[str] = []
priority: list[str] = []

for path in paths:
    rel = relative(path)
    for line_number, kind, block in sentences(path):
        attributes = []
        for line in block.splitlines():
            # Attribute-bearing lines in this source never need a comment
            # suffix. Removing it prevents prose such as "[no-evaluators]"
            # from being mistaken for a declaration attribute.
            code = strip_line_comment(line).rstrip()
            if match := attribute_line_re.search(code):
                attributes.extend(attribute_name_re.findall(match.group(1)))
        attribute_counts.update(attributes)
        kind_counts[kind] += 1
        if path.name == "verification.k":
            disposition = (
                "PROOF_LOCAL_DECLARATION"
                if kind == "syntax"
                else "PROOF_LOCAL_EXACT_EQUATION"
            )
        elif path.name == "spec.k":
            disposition = "POSITIVE_PROOF_OBLIGATION"
        elif "no-evaluators" in attributes:
            disposition = "FIXED_OPAQUE_UNUSED_NO_DEPENDENT_CLAIM"
        elif line_number in used.get(rel, set()):
            disposition = "FIXED_USED_REVIEWED_FAITHFUL"
        elif kind in {"syntax", "configuration"}:
            disposition = "FIXED_DECLARATION_OR_CONFIGURATION"
        else:
            disposition = "FIXED_OUT_OF_PATH_NO_REACHABLE_MATCH"
        if "no-evaluators" in attributes:
            opaque.append(f"{rel}:{line_number}")
        if "priority" in attributes:
            priority.append(f"{rel}:{line_number}")
        all_sentences.append(
            (rel, line_number, kind, block, attributes, disposition)
        )

out: list[str] = []
out.append("# Exhaustive K source sentence inventory")
out.append("")
out.append(
    "Scope: the recursively identical supplied semantics, candidate "
    "`verification.k`, and both candidate claims in `spec.k`."
)
out.append("")
out.append("## Summary")
out.append("")
out.append(f"- Files: {len(paths)}")
out.append(f"- Sentences: {len(all_sentences)}")
for kind, count in sorted(kind_counts.items()):
    out.append(f"- `{kind}` sentences: {count}")
out.append(f"- `[priority]` sentences: {len(priority)}")
out.append(f"- `[no-evaluators]` opaque declarations: {len(opaque)}")
out.append(f"- `[simplification]` attributes: {attribute_counts['simplification']}")
out.append(f"- `[functional]` attributes: {attribute_counts['functional']}")
out.append("")
out.append("Attribute-token counts: " + ", ".join(
    f"`{name}`={count}" for name, count in sorted(attribute_counts.items())
))
out.append("")
out.append("Opaque declarations: " + (", ".join(opaque) if opaque else "none"))
out.append("")
out.append("Priority sentences: " + (", ".join(priority) if priority else "none"))
out.append("")
out.append("## Source hashes")
out.append("")
for path in paths:
    out.append(f"- `{relative(path)}`: `{sha256(path)}`")
out.append("")
out.append("## Every local sentence")
out.append("")
for rel, line_number, kind, block, attributes, disposition in all_sentences:
    out.append(f"### {rel}:{line_number} — {kind}")
    out.append("")
    out.append(f"Disposition: `{disposition}`")
    out.append("")
    out.append(
        "Attributes: "
        + (", ".join(f"`{attribute}`" for attribute in attributes) if attributes else "none")
    )
    out.append("")
    out.append("```k")
    out.append(block)
    out.append("```")
    out.append("")

OUTPUT.write_text("\n".join(out), encoding="utf-8")
print(f"inventory_output={OUTPUT}")
print(f"files={len(paths)}")
print(f"sentences={len(all_sentences)}")
print("kind_counts=" + ",".join(f"{key}:{value}" for key, value in sorted(kind_counts.items())))
print(f"priority_sentences={len(priority)}")
print(f"opaque_no_evaluators={len(opaque)}")
print(f"simplification_attributes={attribute_counts['simplification']}")
print(f"functional_attributes={attribute_counts['functional']}")
print(f"inventory_sha256={sha256(OUTPUT)}")
