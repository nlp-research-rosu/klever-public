#!/usr/bin/env python3
"""Exhaustive source-level K declaration/rule inventory for this audit."""

from __future__ import annotations

import hashlib
import re
from collections import Counter, defaultdict
from pathlib import Path


SEMANTICS_ROOT = Path("/reference/reference-semantics")
SOURCES = [SEMANTICS_ROOT / "semantics.k"] + sorted(
    (SEMANTICS_ROOT / "semantics").glob("*.k")
) + [Path("/candidate/verification.k"), Path("/candidate/spec.k")]

START = re.compile(
    r"^(?:|  )(requires|module|imports|configuration|syntax|context|rule|claim|endmodule)\b"
)

# Rules exercised by the submitted target's proof path. Other supplied rules
# are inventoried but their LHS constructs/values cannot occur in this program.
RELEVANT_FIXED_RULES = {
    ("semantics/core.k", 125),  # #loadAll
    ("semantics/core.k", 126),  # statement sequencing
    ("semantics/core.k", 127),  # empty statements
    ("semantics/core.k", 131),  # Name -> #look
    ("semantics/core.k", 132),  # successful plain lookup
    ("semantics/core.k", 158),  # builtinsScope normalization
    ("semantics/core.k", 189),  # evaluate one argument
    ("semantics/core.k", 190),  # collect evaluated argument
    ("semantics/core.k", 191),  # apply after all arguments
    ("semantics/core.k", 194),  # Int literal
    ("semantics/core.k", 200),  # truthiness of Bool
    ("semantics/core.k", 214),  # append first/only argument
    ("semantics/core.k", 215),  # append recursion
    ("semantics/str.k", 8),  # exhausted string iterator
    ("semantics/str.k", 9),  # yield next string character
    ("semantics/str.k", 14),  # Str literal
    ("semantics/str.k", 15),  # empty literal codes
    ("semantics/str.k", 16),  # nonempty ASCII literal codes
    ("semantics/str.k", 25),  # string equality
    ("semantics/operators.k", 17),  # comparison dispatch
    ("semantics/int.k", 9),  # integer addition
    ("semantics/int.k", 22),  # integer <
    ("semantics/int.k", 26),  # integer ==
    ("semantics/controls.k", 9),  # plain assignment
    ("semantics/controls.k", 20),  # integer augmented assignment
    ("semantics/controls.k", 52),  # If -> Boolean branch
    ("semantics/controls.k", 53),  # true branch
    ("semantics/controls.k", 54),  # false branch
    ("semantics/controls.k", 69),  # For -> #loop
    ("semantics/controls.k", 71),  # iterator request
    ("semantics/controls.k", 72),  # loop completion
    ("semantics/controls.k", 73),  # yielded iteration
    ("semantics/controls.k", 85),  # loop continuation label
    ("semantics/tuple.k", 32),  # plain Name loop-target binding
    ("semantics/functions.k", 14),  # function definition binding
    ("semantics/functions.k", 63),  # no parameters remain
    ("semantics/functions.k", 64),  # bind string parameter
    ("semantics/functions.k", 78),  # return
    ("semantics/functions.k", 85),  # pop frame
    ("semantics/call.k", 20),  # evaluate callee
    ("semantics/call.k", 21),  # evaluate arguments
    ("semantics/call.k", 69),  # enter plain closure
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_name(path: Path) -> str:
    try:
        return path.relative_to(SEMANTICS_ROOT).as_posix()
    except ValueError:
        return f"candidate/{path.name}"


def blocks(path: Path):
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    for number, (index, kind) in enumerate(starts):
        next_index = starts[number + 1][0] if number + 1 < len(starts) else len(lines)
        block_lines = lines[index:next_index]
        while block_lines and (
            not block_lines[-1].strip() or block_lines[-1].lstrip().startswith("//")
        ):
            block_lines.pop()
        yield index + 1, kind, "\n".join(block_lines)


def tags(text: str) -> list[str]:
    result = []
    for tag, pattern in [
        ("function", r"\bfunction\b"),
        ("total", r"\btotal\b"),
        ("functional", r"\bfunctional\b"),
        ("opaque/no-evaluators", r"\bno-evaluators\b"),
        ("concrete", r"\bconcrete\b"),
        ("priority", r"\bpriority\s*\("),
        ("simplification", r"\bsimplification\b"),
        ("owise", r"\bowise\b"),
        ("macro", r"\bmacro(?:-rec)?\b"),
        ("strict", r"\b(?:seq)?strict(?:\s*\(|\b)"),
    ]:
        if re.search(pattern, text):
            result.append(tag)
    return result


def rule_scope(relative: str, line: int, kind: str) -> str:
    if relative == "candidate/verification.k":
        return "PROOF_LOCAL_EXTENSION"
    if relative == "candidate/spec.k":
        return "TARGET_CLAIM"
    if relative == "semantics/concrete.k":
        return "SUPPLIED_CONCRETE_ONLY"
    if kind == "rule" and (relative, line) in RELEVANT_FIXED_RULES:
        return "SUPPLIED_FIXED_REACHED"
    if kind == "rule":
        return "SUPPLIED_FIXED_UNREACHED"
    return "DECLARATION"


def main() -> int:
    counts: Counter[str] = Counter()
    tags_count: Counter[str] = Counter()
    per_file: dict[str, Counter[str]] = defaultdict(Counter)
    records: list[tuple[str, int, str, str, list[str], str]] = []
    for path in SOURCES:
        relative = source_name(path)
        for line, kind, text in blocks(path):
            compact = " ".join(part.strip() for part in text.splitlines() if part.strip())
            block_tags = tags(text)
            scope = rule_scope(relative, line, kind)
            records.append((relative, line, kind, scope, block_tags, compact))
            counts[kind] += 1
            per_file[relative][kind] += 1
            tags_count.update(block_tags)

    print("# Exhaustive K source inventory")
    print()
    print("Every top-level source declaration, context, rule, and claim is listed once.")
    print(
        "`SUPPLIED_FIXED_UNREACHED` means its LHS construct/value cannot arise in "
        "the submitted target; it remains part of the supplied-semantics trust boundary."
    )
    print()
    print("## Source hashes and counts")
    print()
    for path in SOURCES:
        relative = source_name(path)
        rendered = ", ".join(
            f"{kind}={count}" for kind, count in sorted(per_file[relative].items())
        )
        print(f"- {relative}: sha256={digest(path)}; {rendered}")
    print()
    print("## Aggregate counts")
    print()
    print("- kinds: " + ", ".join(f"{key}={value}" for key, value in sorted(counts.items())))
    print(
        "- attributes: "
        + ", ".join(f"{key}={value}" for key, value in sorted(tags_count.items()))
    )
    print()
    print("## Inventory")
    print()
    for relative, line, kind, scope, block_tags, compact in records:
        rendered_tags = ",".join(block_tags) if block_tags else "-"
        print(
            f"- {relative}:{line} | {kind} | {scope} | attrs={rendered_tags} | "
            f"{compact}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
