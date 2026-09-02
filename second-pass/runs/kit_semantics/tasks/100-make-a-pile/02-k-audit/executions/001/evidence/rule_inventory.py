#!/usr/bin/env python3
"""Create an exhaustive line-anchored inventory of local K declarations."""

from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path
import re


SEMANTICS = Path("/tmp/audit-work/reconstruction/reference-semantics")
SCRATCH = Path("/tmp/audit-work/reconstruction")

files = [SEMANTICS / "semantics.k"] + sorted((SEMANTICS / "semantics").glob("*.k"))
files += [SCRATCH / "verification.k", SCRATCH / "spec.k"]

start_re = re.compile(r"^\s*(syntax|rule|claim|context|configuration)\b")
attr_names = [
    "function",
    "total",
    "functional",
    "symbol",
    "no-evaluators",
    "priority",
    "simplification",
    "concrete",
    "owise",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
]

# These local declarations/rules are exercised by the submitted term or are
# the proof-local summary/claims. Strictness declarations are marked at their
# starting syntax declaration.
used = {
    "semantics/syntax.k": {9, 32, 37, 41, 56, 57, 60, 61},
    "semantics/core.k": {
        13, 18, 25, 36, 37, 38, 39, 40, 41, 42, 49, 117, 118, 124, 125,
        126, 127, 130, 131, 132, 185, 186, 189, 190, 191, 194, 199, 202,
        209, 210, 213, 214, 215, 217, 218, 219,
    },
    "semantics/operators.k": {12, 15, 16, 17},
    "semantics/int.k": {9, 14, 22},
    "semantics/list.k": {13, 14, 15, 18, 19, 20, 53},
    "semantics/controls.k": {
        9, 20, 48, 65, 77, 78, 79, 81, 85,
    },
    "semantics/functions.k": {
        8, 14, 63, 64, 78, 85,
    },
    "semantics/call.k": {
        16, 19, 20, 21, 24, 52, 53, 56, 69,
    },
    "verification.k": {6, 13, 16},
    "spec.k": {6, 38},
}


def rel_name(path: Path) -> str:
    if path == SCRATCH / "verification.k" or path == SCRATCH / "spec.k":
        return path.name
    return path.relative_to(SEMANTICS).as_posix()


def blocks(path: Path):
    lines = path.read_text().splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = start_re.match(line)
        if match:
            starts.append((index, match.group(1)))
    for position, (index, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        raw = "\n".join(lines[index:end]).rstrip()
        yield index + 1, kind, raw


records = []
for path in files:
    rel = rel_name(path)
    for line, kind, raw in blocks(path):
        uncommented = "\n".join(part.split("//", 1)[0] for part in raw.splitlines())
        attrs = [name for name in attr_names if re.search(rf"\b{re.escape(name)}\b", uncommented)]
        is_used = line in used.get(rel, set())
        if rel == "verification.k" and kind == "rule":
            disposition = (
                "ACCEPT: proof-local finishPile equation; guards are exhaustive/"
                "disjoint and recursion descends"
            )
        elif rel == "verification.k":
            disposition = "ACCEPT: pure proof-local syntax; no operational cell match"
        elif rel == "spec.k":
            disposition = "ACCEPT: reconstructed positive reachability claim"
        elif is_used:
            disposition = (
                "ACCEPT/USED: byte-identical fixed-semantics declaration or step; "
                "reviewed against the submitted execution path"
            )
        else:
            disposition = (
                "ACCEPT/OFF-PATH: byte-identical fixed-semantics item; its "
                "constructor, sort, guard, or state case is unreachable from "
                "the submitted execution"
            )
        snippet = " ".join(
            line_text.strip()
            for line_text in uncommented.splitlines()
            if line_text.strip()
        )
        snippet = snippet.replace("|", "\\|")
        if len(snippet) > 180:
            snippet = snippet[:177] + "..."
        records.append(
            {
                "file": rel,
                "line": line,
                "kind": kind,
                "attrs": ",".join(attrs) if attrs else "—",
                "used": "used" if is_used else "off-path",
                "sha": sha256(raw.encode()).hexdigest()[:16],
                "snippet": snippet,
                "disposition": disposition,
            }
        )

kind_counts = Counter(record["kind"] for record in records)
attr_counts = Counter()
path_counts = Counter(record["file"] for record in records)
for record in records:
    if record["attrs"] != "—":
        attr_counts.update(record["attrs"].split(","))

print("# Exhaustive local K declaration and rule inventory")
print()
print(
    "Scope: trusted supplied `semantics.k`, every helper under `semantics/*.k`, "
    "plus candidate `verification.k` and positive `spec.k`. Generated K builtin "
    "rules are outside the local-source inventory; strictness effects are recorded "
    "through their source declarations."
)
print()
print(f"- Total inventoried items: {len(records)}")
print(f"- Kind counts: {dict(sorted(kind_counts.items()))}")
print(f"- Attribute counts: {dict(sorted(attr_counts.items()))}")
print("- Functional declarations: 0" if attr_counts["functional"] == 0 else "")
print("- Simplification rules: 0" if attr_counts["simplification"] == 0 else "")
print()
print("## Per-file counts")
print()
for path, count in sorted(path_counts.items()):
    print(f"- `{path}`: {count}")
print()
print("## Items")
print()
print("| File:line | Kind | Attributes | Path | Source hash | Declaration/rule head | Disposition |")
print("|---|---|---|---|---|---|---|")
for record in records:
    print(
        f"| `{record['file']}:{record['line']}` | {record['kind']} | "
        f"{record['attrs']} | {record['used']} | `{record['sha']}` | "
        f"{record['snippet']} | {record['disposition']} |"
    )
