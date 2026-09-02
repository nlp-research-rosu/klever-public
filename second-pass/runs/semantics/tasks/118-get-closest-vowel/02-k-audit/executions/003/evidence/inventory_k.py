#!/usr/bin/env python3
"""Generate a line-addressed inventory of every K declaration and rule."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re


ROOTS = [
    Path("/reference/reference-semantics/semantics.k"),
    *sorted(Path("/reference/reference-semantics/semantics").glob("*.k")),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]
OUTPUT = Path("/audit-output/evidence/rule_inventory.md")
START = re.compile(
    r"^\s*(configuration|syntax|rule|claim|context(?:\s+alias)?|alias)\b"
)
BOUNDARY = re.compile(
    r"^\s*(configuration|syntax|rule|claim|context(?:\s+alias)?|alias|module|endmodule|imports)\b"
)


def clean(block: list[str]) -> str:
    pieces: list[str] = []
    for line in block:
        stripped = line.strip()
        if not stripped or stripped.startswith("//"):
            continue
        pieces.append(stripped.replace("|", r"\|"))
    return " ".join(pieces)


def attributes(text: str) -> str:
    found = []
    for name in [
        "macro",
        "function",
        "functional",
        "total",
        "symbol",
        "no-evaluators",
        "simplification",
        "priority",
        "owise",
        "strict",
        "seqstrict",
    ]:
        if re.search(rf"\b{re.escape(name)}\b", text):
            found.append(name)
    return ", ".join(found) if found else "ordinary"


def main() -> None:
    output: list[str] = [
        "# Exhaustive K declaration and rule inventory",
        "",
        "Generated independently from the trusted supplied-semantics mount and "
        "the candidate's `verification.k`/`spec.k`. Each entry gives the exact "
        "source span and a flattened rendering; the source files remain authoritative.",
        "",
    ]
    global_counts: Counter[str] = Counter()
    identifier = 0

    for path in ROOTS:
        lines = path.read_text(encoding="utf-8").splitlines()
        entries: list[tuple[str, int, int, str]] = []
        starts = [
            index
            for index, line in enumerate(lines)
            if START.match(line)
        ]
        for position, start in enumerate(starts):
            match = START.match(lines[start])
            assert match is not None
            kind = match.group(1).replace(" ", "-")
            end_limit = starts[position + 1] if position + 1 < len(starts) else len(lines)
            end = end_limit
            # Do not absorb module terminators/imports into the declaration.
            for index in range(start + 1, end_limit):
                if BOUNDARY.match(lines[index]):
                    end = index
                    break
            while end > start + 1 and (
                not lines[end - 1].strip() or lines[end - 1].lstrip().startswith("//")
            ):
                end -= 1
            text = clean(lines[start:end])
            entries.append((kind, start + 1, end, text))

        rel = (
            str(path.relative_to("/reference/reference-semantics"))
            if str(path).startswith("/reference/reference-semantics/")
            else str(path)
        )
        counts = Counter(kind for kind, *_ in entries)
        global_counts.update(counts)
        output.extend(
            [
                f"## `{rel}`",
                "",
                f"Entries: {len(entries)}; counts: {dict(sorted(counts.items()))}",
                "",
            ]
        )
        for kind, start, end, text in entries:
            identifier += 1
            attr = attributes(text)
            output.append(
                f"- K{identifier:04d} `{kind}` `{path}:{start}-{end}` "
                f"[{attr}] — `{text}`"
            )
        output.append("")

    opaque = []
    priority = []
    simplification = []
    for path in ROOTS:
        for line_number, line in enumerate(path.read_text().splitlines(), 1):
            stripped = line.strip()
            if not stripped.startswith("//") and ("symbol(" in line or "no-evaluators" in line):
                opaque.append(f"`{path}:{line_number}` — `{line.strip()}`")
            if not stripped.startswith("//") and "priority(" in line:
                priority.append(f"`{path}:{line_number}` — `{line.strip()}`")
            if not stripped.startswith("//") and "simplification" in line:
                simplification.append(f"`{path}:{line_number}` — `{line.strip()}`")

    output.extend(
        [
            "# Cross-cutting attribute indexes",
            "",
            f"Total inventoried entries: {identifier}; global counts: "
            f"{dict(sorted(global_counts.items()))}",
            "",
            "## Opaque/external-symbol declarations (`symbol` or `no-evaluators`)",
            "",
            *(f"- {entry}" for entry in opaque),
            "",
            "## Priority occurrences",
            "",
            *(f"- {entry}" for entry in priority),
            "",
            "## Simplification occurrences",
            "",
            *(f"- {entry}" for entry in simplification),
            "",
        ]
    )
    OUTPUT.write_text("\n".join(output), encoding="utf-8")
    print(f"wrote={OUTPUT}")
    print(f"files={len(ROOTS)}")
    print(f"entries={identifier}")
    print(f"counts={dict(sorted(global_counts.items()))}")
    print(f"opaque_or_external={len(opaque)}")
    print(f"priority_occurrences={len(priority)}")
    print(f"simplification_occurrences={len(simplification)}")


if __name__ == "__main__":
    main()
