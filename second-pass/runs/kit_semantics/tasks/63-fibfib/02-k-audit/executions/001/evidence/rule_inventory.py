"""Line-faithful inventory of the supplied MPY theory and proof-local theory.

This is intentionally a lexical inventory rather than a K parser: every
top-level declaration is retained with its exact source span and text, making
omissions easy to check against `rg`/source line counts.
"""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work")
SEMANTICS = ROOT / "reference-semantics"
FILES = [
    SEMANTICS / "semantics.k",
    *sorted((SEMANTICS / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]

TOP_LEVEL_REQUIRES = re.compile(r"^(requires)\b")
START = re.compile(
    r"^\s*(module|endmodule|imports|configuration|syntax|context|rule|claim)\b"
)
INTERESTING = (
    "function",
    "total",
    "functional",
    "symbol(",
    "no-evaluators",
    "priority(",
    "simplification",
    "concrete",
    "owise",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
)


def declaration_flags(text: str):
    code_lines = [line.split("//", 1)[0] for line in text.splitlines()]
    attribute_text = " ".join(
        re.findall(r"\[([^\]]*)\]", "\n".join(code_lines), flags=re.DOTALL)
    )
    flags = []
    for flag in INTERESTING:
        if flag.endswith("("):
            present = flag in attribute_text
        else:
            present = re.search(
                rf"(?<![A-Za-z0-9_-]){re.escape(flag)}(?![A-Za-z0-9_-])",
                attribute_text,
            )
        if present:
            flags.append(flag)
    return flags


def declarations(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = TOP_LEVEL_REQUIRES.match(line) or START.match(line)
        if match is not None:
            starts.append((index, match.group(1)))
    for position, (start, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        # Drop trailing blank/comment-only lines before the next declaration.
        block = lines[start:end]
        while block and (not block[-1].strip() or block[-1].lstrip().startswith("//")):
            block.pop()
        yield kind, start + 1, start + len(block), "\n".join(block)


counts: collections.Counter[str] = collections.Counter()
flag_counts: collections.Counter[str] = collections.Counter()
ordinal = 0
for path in FILES:
    relative = path.relative_to(ROOT)
    print(f"\n=== FILE {relative} ===")
    for kind, start, end, text in declarations(path):
        ordinal += 1
        counts[kind] += 1
        flags = declaration_flags(text)
        for flag in flags:
            flag_counts[flag] += 1
        one_line = " ".join(part.strip() for part in text.splitlines())
        print(
            f"{ordinal:04d} {relative}:{start}-{end} "
            f"KIND={kind} FLAGS={','.join(flags) if flags else '-'}"
        )
        print(f"  {one_line}")

print("\n=== SUMMARY ===")
print(f"FILES={len(FILES)}")
print(f"DECLARATIONS={ordinal}")
for kind, count in sorted(counts.items()):
    print(f"KIND {kind} {count}")
for flag, count in sorted(flag_counts.items()):
    print(f"FLAG {flag} {count}")
