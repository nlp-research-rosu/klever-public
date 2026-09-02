#!/usr/bin/env python3
"""Generate a source-addressed inventory of all K declarations and sentences."""

from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
from pathlib import Path
import re


WORK = Path("/tmp/audit-work/160-do-algebra")
OUTPUT = Path("/audit-output/evidence/stage5/RULE_INVENTORY.md")
FILES = [
    WORK / "reference-semantics/semantics.k",
    *sorted((WORK / "reference-semantics/semantics").glob("*.k")),
    WORK / "verification.k",
    WORK / "spec.k",
]

START = re.compile(r"^\s*(configuration|syntax|rule|claim|context|alias)\b")
BOUNDARY = re.compile(r"^\s*(module|endmodule|imports)\b")
ATTR = re.compile(r"\[([^\]]+)\]")
KNOWN_ATTR_PREFIXES = (
    "function",
    "total",
    "functional",
    "macro",
    "macro-rec",
    "symbol",
    "no-evaluators",
    "strict",
    "seqstrict",
    "owise",
    "priority",
    "concrete",
    "simplification",
    "hook",
    "token",
    "assoc",
    "comm",
    "unit",
    "idem",
    "left",
    "right",
    "bracket",
    "klabel",
    "format",
)


def compact(text: str, limit: int = 460) -> str:
    text = re.sub(r"\s+", " ", text.strip()).replace("|", r"\|")
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


records: list[dict[str, object]] = []
for path in FILES:
    lines = path.read_text().splitlines()
    starts = [i for i, line in enumerate(lines) if START.match(line)]
    for position, start in enumerate(starts):
        # Stop at the next declaration/sentence. Module/import boundaries are
        # naturally before the next item and do not affect sentence attributes.
        stop = starts[position + 1] if position + 1 < len(starts) else len(lines)
        for index in range(start + 1, stop):
            if BOUNDARY.match(lines[index]) and not START.match(lines[index]):
                stop = index
                break
        sentence_lines = lines[start:stop]
        for offset, line in enumerate(sentence_lines[1:], 1):
            if not line.strip():
                sentence_lines = sentence_lines[:offset]
                break
        chunk = "\n".join(sentence_lines).strip()
        match = START.match(lines[start])
        assert match is not None
        kind = match.group(1)
        attributes: list[str] = []
        for group in ATTR.findall(chunk):
            tokens = [token.strip() for token in group.split(",") if token.strip()]
            if tokens and all(token.startswith(KNOWN_ATTR_PREFIXES) for token in tokens):
                attributes.extend(tokens)
        attributes = sorted(set(attributes))
        if kind == "rule":
            if any(attr.startswith("priority") for attr in attributes):
                rule_class = "priority rule"
            elif "owise" in attributes:
                rule_class = "owise rule"
            elif "simplification" in attributes or any(
                attr.startswith("simplification") for attr in attributes
            ):
                rule_class = "simplification rule"
            elif "concrete" in attributes:
                rule_class = "concrete rule"
            else:
                rule_class = "ordinary rule"
        elif kind == "syntax":
            flags = [
                flag
                for flag in (
                    "function",
                    "total",
                    "functional",
                    "macro",
                    "macro-rec",
                    "symbol",
                    "no-evaluators",
                )
                if flag in attributes
            ]
            rule_class = "syntax" + (f" ({', '.join(flags)})" if flags else "")
        else:
            rule_class = kind
        records.append(
            {
                "file": path.relative_to(WORK).as_posix(),
                "line": start + 1,
                "kind": kind,
                "class": rule_class,
                "attrs": ", ".join(attributes) if attributes else "—",
                "digest": hashlib.sha256(chunk.encode()).hexdigest()[:12],
                "sentence": compact(chunk),
            }
        )

counts = Counter(str(record["kind"]) for record in records)
classes = Counter(str(record["class"]) for record in records)
per_file = defaultdict(Counter)
for record in records:
    per_file[str(record["file"])][str(record["kind"])] += 1

with OUTPUT.open("w", encoding="utf-8") as stream:
    stream.write("# Exhaustive K source inventory\n\n")
    stream.write(
        "Generated from the clean scratch copies. Each row is keyed by source line "
        "and a digest of the full declaration/sentence; displayed text is bounded.\n\n"
    )
    stream.write(f"- Files: {len(FILES)}\n")
    stream.write(f"- Total inventory records: {len(records)}\n")
    stream.write(f"- Kinds: `{dict(sorted(counts.items()))}`\n")
    stream.write(f"- Classes: `{dict(sorted(classes.items()))}`\n\n")
    stream.write("## Per-file counts\n\n")
    stream.write("| File | configuration | syntax | context | rule | claim | alias |\n")
    stream.write("|---|---:|---:|---:|---:|---:|---:|\n")
    for file_name in sorted(per_file):
        count = per_file[file_name]
        stream.write(
            f"| `{file_name}` | {count['configuration']} | {count['syntax']} | "
            f"{count['context']} | {count['rule']} | {count['claim']} | {count['alias']} |\n"
        )
    stream.write("\n## Source-addressed inventory\n\n")
    stream.write("| Location | Kind/class | Attributes | Digest | Full-sentence prefix |\n")
    stream.write("|---|---|---|---|---|\n")
    for record in records:
        stream.write(
            f"| `{record['file']}:{record['line']}` | {record['class']} | "
            f"{record['attrs']} | `{record['digest']}` | {record['sentence']} |\n"
        )

print(f"output={OUTPUT}")
print(f"files={len(FILES)} records={len(records)}")
print(f"kinds={dict(sorted(counts.items()))}")
print(f"classes={dict(sorted(classes.items()))}")
print(f"sha256={hashlib.sha256(OUTPUT.read_bytes()).hexdigest()}")
