#!/usr/bin/env python3
"""Emit an exhaustive source-level inventory of K declarations and rules."""

from __future__ import annotations

import collections
import re
import sys
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
KEYWORDS = (
    "requires",
    "module",
    "endmodule",
    "imports",
    "configuration",
    "syntax",
    "context",
    "rule",
    "claim",
)
START = re.compile(
    r"^(?:(requires)(?=\s+\")|(module)\b|(endmodule)\b|"
    r"\s*(imports|configuration|syntax|context|rule|claim)\b)"
)


def strip_comments(text: str) -> str:
    """Remove K comments without mistaking the quoted Python operator "//"."""
    output: list[str] = []
    index = 0
    in_string = False
    escaped = False
    while index < len(text):
        char = text[index]
        following = text[index + 1] if index + 1 < len(text) else ""
        if in_string:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
        elif char == '"':
            in_string = True
            output.append(char)
            index += 1
        elif char == "/" and following == "/":
            index += 2
            while index < len(text) and text[index] != "\n":
                index += 1
        elif char == "/" and following == "*":
            index += 2
            while index + 1 < len(text) and text[index : index + 2] != "*/":
                if text[index] == "\n":
                    output.append("\n")
                index += 1
            index += 2
        else:
            output.append(char)
            index += 1
    return "".join(output)


def statements(path: Path):
    lines = strip_comments(path.read_text()).splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, next(group for group in match.groups() if group)))
    for item_index, (start, kind) in enumerate(starts):
        end = starts[item_index + 1][0] if item_index + 1 < len(starts) else len(lines)
        body = "\n".join(lines[start:end]).strip()
        # module/import/require/end markers are always single-line statements.
        if kind in {"requires", "module", "endmodule", "imports"}:
            body = lines[start].strip()
        yield start + 1, kind, body


def status_for(path: Path, kind: str) -> str:
    rel = path.relative_to(ROOT)
    if rel.parts[0] == "reference-semantics":
        return "TRUSTED_SUPPLIED"
    if rel.name in {
        "verification-base.k",
        "verification.k",
        "arithmetic-verification.k",
    }:
        if kind in {"syntax", "rule", "context", "configuration"}:
            return "PROOF_EXTENSION_MANUAL"
        return "PROOF_MODULE_STRUCTURE"
    if "mutation" in rel.name or rel.name == "spec-vacuity.k":
        return "NEGATIVE_PROBE_NOT_POSITIVE_THEORY"
    if kind == "claim":
        return "POSITIVE_CLAIM_RECONSTRUCTED"
    return "SPEC_MODULE_STRUCTURE"


def main() -> int:
    files = sorted((ROOT / "reference-semantics").rglob("*.k"))
    files.extend(
        ROOT / name
        for name in (
            "verification-base.k",
            "verification.k",
            "arithmetic-verification.k",
            "arithmetic-spec.k",
            "connection-spec.k",
            "rounding-spec.k",
            "spec.k",
            "spec-body-mutation.k",
            "spec-vacuity.k",
            "connection-body-mutation.k",
        )
    )
    counter: collections.Counter[tuple[str, str]] = collections.Counter()
    attributes: collections.Counter[str] = collections.Counter()
    item_number = 0
    print("# Exhaustive K source inventory")
    print()
    print(
        "Status legend: TRUSTED_SUPPLIED is the recursively verified fixed "
        "SUPPLIED_SEMANTICS baseline; PROOF_EXTENSION_MANUAL entries receive "
        "rule-by-rule reasoning in REVIEW.md; claims are independently rebuilt."
    )
    for path in files:
        rel = path.relative_to(ROOT)
        print()
        print(f"## {rel}")
        file_items = list(statements(path))
        print(f"Source statements: {len(file_items)}")
        for line, kind, body in file_items:
            item_number += 1
            status = status_for(path, kind)
            counter[(status, kind)] += 1
            found_attributes = re.findall(r"\[([^\]]+)\]", body)
            known_attributes = {
                "anywhere",
                "assoc",
                "avoid",
                "bracket",
                "cell",
                "comm",
                "concrete",
                "format",
                "function",
                "functional",
                "hook",
                "idem",
                "left",
                "macro",
                "macro-rec",
                "maincell",
                "no-evaluators",
                "owise",
                "priority",
                "right",
                "seqstrict",
                "simplification",
                "stream",
                "strict",
                "symbol",
                "symbolic",
                "token",
                "total",
                "unit",
            }
            for found in found_attributes:
                for attribute in found.split(","):
                    attribute_name = attribute.strip().split("(")[0]
                    if attribute_name in known_attributes:
                        attributes[attribute_name] += 1
            compact = " ".join(body.split())
            # Do not truncate: the evidence file is the exhaustive declaration.
            print(
                f"{item_number:04d}. line {line}; kind={kind}; "
                f"status={status}; text=`{compact}`"
            )
    print()
    print("# Counts")
    print(f"TOTAL_STATEMENTS={item_number}")
    for (status, kind), count in sorted(counter.items()):
        print(f"{status} {kind} {count}")
    print("ATTRIBUTES")
    for attribute, count in sorted(attributes.items()):
        print(f"{attribute} {count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
