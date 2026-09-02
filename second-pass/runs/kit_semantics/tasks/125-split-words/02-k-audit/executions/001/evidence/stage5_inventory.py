#!/usr/bin/env python3
"""Sentence-by-sentence K source inventory with reachability classification."""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/125-split-words")
SEMANTICS = ROOT / "reference-semantics"
FILES = [
    SEMANTICS / "semantics.k",
    *sorted((SEMANTICS / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]

# Inclusive line ranges whose declarations/rules participate in this program's
# syntax or fixed-semantics execution. Other supplied rules have disjoint heads
# or constructors and cannot fire on this program.
ACTIVE_RANGES: dict[str, list[tuple[int, int]]] = {
    "semantics/syntax.k": [
        (9, 17),
        (28, 32),
        (37, 37),
        (41, 41),
        (49, 53),
        (56, 61),
    ],
    "semantics/core.k": [
        (13, 42),
        (49, 60),
        (68, 70),
        (117, 132),
        (152, 191),
        (194, 210),
        (218, 220),
        (238, 254),
    ],
    "semantics/functions.k": [(8, 20), (62, 90)],
    "semantics/call.k": [(15, 24), (52, 60), (69, 74)],
    "semantics/controls.k": [(8, 18), (46, 54)],
    "semantics/operators.k": [(10, 17), (22, 46)],
    "semantics/bool.k": [(24, 36)],
    "semantics/int.k": [(7, 12), (22, 23), (31, 36)],
    "semantics/str.k": [(13, 41)],
    "semantics/list.k": [(12, 28)],
    "semantics/methods.k": [(9, 44), (63, 102)],
}

START = re.compile(r"^\s*(syntax|rule|claim|configuration|context|alias)\b")
ATTRS = [
    "function",
    "total",
    "functional",
    "simplification",
    "priority",
    "owise",
    "concrete",
    "no-evaluators",
    "macro",
    "macro-rec",
]


def rel(path: Path) -> str:
    if path == ROOT / "verification.k" or path == ROOT / "spec.k":
        return path.name
    return path.relative_to(SEMANTICS).as_posix()


def sentence_starts(lines: list[str]) -> list[int]:
    return [index for index, line in enumerate(lines) if START.match(line)]


def active(path_name: str, line: int) -> bool:
    return any(lo <= line <= hi for lo, hi in ACTIVE_RANGES.get(path_name, []))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


items: list[dict[str, object]] = []
file_counts: Counter[str] = Counter()
kind_counts: Counter[str] = Counter()
attr_counts: Counter[str] = Counter()
class_counts: Counter[str] = Counter()

for path in FILES:
    lines = path.read_text().splitlines()
    starts = sentence_starts(lines)
    path_name = rel(path)
    print(f"READ_FILE {path_name} lines={len(lines)} sha256={sha256(path)}")
    for ordinal, start in enumerate(starts):
        stop = starts[ordinal + 1] if ordinal + 1 < len(starts) else len(lines)
        # Do not absorb the next module boundary into a sentence.
        for candidate in range(start + 1, stop):
            if re.match(r"^\s*endmodule\b", lines[candidate]):
                stop = candidate
                break
        text = " ".join(
            piece.strip()
            for piece in lines[start:stop]
            if piece.strip() and not piece.lstrip().startswith("//")
        )
        match = START.match(lines[start])
        assert match
        kind = match.group(1)
        found_attrs = [attr for attr in ATTRS if re.search(rf"\b{re.escape(attr)}\b", text)]
        line_number = start + 1
        if path_name == "verification.k":
            classification = "PROOF_LOCAL_REVIEWED"
            verdict = (
                "TRANSPARENT_DEFINITION_REVIEWED_TRUE"
                if kind in {"syntax", "rule"}
                else "REVIEWED"
            )
        elif path_name == "spec.k":
            classification = "POSITIVE_TARGET"
            verdict = "TARGET_NOT_IMPORTED_AS_AXIOM"
        elif active(path_name, line_number):
            classification = "ACTIVE_FIXED_SEMANTICS"
            verdict = (
                "DECLARATION"
                if kind in {"syntax", "configuration", "context"}
                else "REVIEWED_SOUND_ON_REACHABLE_DOMAIN"
            )
        else:
            classification = "INACTIVE_FIXED_SEMANTICS"
            verdict = "DISJOINT_FROM_REACHABLE_PROGRAM_TERMS"
        item = {
            "path": path_name,
            "line": line_number,
            "kind": kind,
            "attrs": found_attrs,
            "classification": classification,
            "verdict": verdict,
            "text": text,
        }
        items.append(item)
        file_counts[path_name] += 1
        kind_counts[kind] += 1
        class_counts[classification] += 1
        attr_counts.update(found_attrs)

print()
print("# Static K sentence inventory")
print()
print(f"Total inventoried sentences: {len(items)}")
print()
print("Kinds:", ", ".join(f"{key}={kind_counts[key]}" for key in sorted(kind_counts)))
print(
    "Attributes:",
    ", ".join(f"{key}={attr_counts[key]}" for key in ATTRS if attr_counts[key]),
)
print(
    "Classifications:",
    ", ".join(f"{key}={class_counts[key]}" for key in sorted(class_counts)),
)
print()
print("Per-file counts:")
for path_name in sorted(file_counts):
    print(f"- {path_name}: {file_counts[path_name]}")
print()
print("## Items")
print()
for index, item in enumerate(items, 1):
    attrs = ",".join(item["attrs"]) if item["attrs"] else "-"
    text = str(item["text"]).replace("|", "\\|")
    print(
        f"{index:04d}. `{item['path']}:{item['line']}` "
        f"kind={item['kind']} attrs={attrs} "
        f"class={item['classification']} verdict={item['verdict']} — `{text}`"
    )
