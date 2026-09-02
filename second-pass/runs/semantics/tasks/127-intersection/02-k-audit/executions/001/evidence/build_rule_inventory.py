#!/usr/bin/env python3
"""Build a line-addressed inventory of all local K declarations and rules."""

from __future__ import annotations

import collections
import re
from pathlib import Path


REFERENCE_ROOT = Path("/tmp/audit-work/candidate/reference-semantics")
VERIFICATION = Path("/tmp/audit-work/candidate/verification.k")
SPEC = Path("/tmp/audit-work/candidate/spec.k")
OUTPUT = Path("/audit-output/evidence/15-rule-inventory.md")

START = re.compile(
    r"^\s*(configuration|syntax|context\s+alias|context|rule|claim)\b"
)
END = re.compile(r"^\s*(?:end)?module\b")
KNOWN_ATTRIBUTES = (
    "function",
    "total",
    "functional",
    "no-evaluators",
    "symbol(",
    "priority(",
    "concrete",
    "owise",
    "simplification",
    "anywhere",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
)


def source_files() -> list[Path]:
    return [
        REFERENCE_ROOT / "semantics.k",
        *sorted((REFERENCE_ROOT / "semantics").glob("*.k")),
        VERIFICATION,
        SPEC,
    ]


def strip_comment(line: str) -> str:
    if line.lstrip().startswith("//"):
        return ""
    return line.rstrip()


def parse_items(path: Path) -> list[dict[str, object]]:
    lines = path.read_text().splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    items = []
    for position, index in enumerate(starts):
        stop = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block_lines = []
        for line in lines[index:stop]:
            if END.match(line):
                break
            cleaned = strip_comment(line)
            if cleaned.strip():
                block_lines.append(cleaned.strip())
        text = " ".join(block_lines)
        text = re.sub(r"\s+", " ", text).strip()
        kind = START.match(lines[index]).group(1).replace(" ", "-")
        attrs = [attribute for attribute in KNOWN_ATTRIBUTES if attribute in text]
        items.append(
            {
                "path": path,
                "line": index + 1,
                "kind": kind,
                "attrs": attrs,
                "text": text,
            }
        )
    return items


def semantic_role(item: dict[str, object]) -> str:
    kind = str(item["kind"])
    text = str(item["text"])
    if kind == "configuration":
        return "configuration"
    if kind.startswith("context"):
        return "evaluation-context"
    if kind == "syntax":
        if "no-evaluators" in text:
            return "opaque-symbol-declaration"
        if "function" in text:
            return "function-declaration"
        if "macro" in text:
            return "macro-declaration"
        return "syntax-declaration"
    if kind == "claim":
        return "reachability-claim"
    if "<k>" in text or "~>" in text or "<scopes>" in text:
        return "operational-rule"
    if "concrete" in text:
        return "concrete-equation"
    return "equation-or-macro-rule"


def decision(item: dict[str, object]) -> tuple[str, str]:
    path = Path(item["path"])
    line = int(item["line"])
    if path == SPEC:
        return (
            "CLAIM",
            "positive theorem obligation; independently rebuilt and audited below",
        )
    if path != VERIFICATION:
        return (
            "ACCEPT_FIXED",
            "byte-identical supplied-semantics baseline; fixed theory, with used-path "
            "rules separately checked for applicability and fidelity",
        )

    if line == 9:
        return (
            "SOUND",
            "Map deletion normalization: removing known key 1 from a disjoint "
            "1-binding plus remainder yields exactly the remainder",
        )
    if line in (15, 37):
        return (
            "SOUND",
            "name-only function declaration for an exact submitted statement list",
        )
    if line in (16, 38):
        return (
            "SOUND",
            "transparent definitional expansion; constructor-for-constructor match "
            "to the trusted regeneration of solution.mpy",
        )
    if line == 46:
        return (
            "SOUND",
            "name-only function declarations for the two concrete result strings",
        )
    if line in (48, 49):
        return (
            "SOUND",
            "transparent ASCII encoding of YES or NO",
        )
    if line == 53:
        return (
            "SOUND",
            "transparent mathematical helper declarations; no opacity or total axiom",
        )
    if line in (55, 57, 59):
        return (
            "SOUND",
            "disjoint, exhaustive divisor-search equations over the reachable "
            "domain D >= 2; recursive case strictly increases D toward N",
        )
    if line in (62, 64):
        return (
            "SOUND",
            "disjoint and exhaustive prime-result equations",
        )
    if line == 67:
        return (
            "SOUND",
            "transparent overlap-length helper declaration",
        )
    if line == 68:
        return (
            "SOUND",
            "closed-interval overlap length min(endpoints)-max(starts), matching "
            "the task's length convention",
        )
    if line == 78:
        return (
            "SOUND_DERIVED",
            "operational loop summary is the independently proved LOOP-SPEC claim "
            "over the same body, suffix, stack, cells, and guard",
        )
    return ("REVIEW", "candidate-local item requires manual classification")


def main() -> None:
    all_items = []
    for path in source_files():
        all_items.extend(parse_items(path))

    kind_counts = collections.Counter(str(item["kind"]) for item in all_items)
    role_counts = collections.Counter(semantic_role(item) for item in all_items)
    attr_counts = collections.Counter()
    decision_counts = collections.Counter()
    for item in all_items:
        attr_counts.update(item["attrs"])
        decision_counts.update([decision(item)[0]])

    out = [
        "# Exhaustive K declaration and rule inventory",
        "",
        "Generated from the fresh scratch source copy. Every local `configuration`, "
        "`syntax`, `context`, `rule`, and `claim` directive is listed once. "
        "Continuation alternatives belonging to a multiline syntax declaration remain "
        "inside that declaration.",
        "",
        f"- Items: {len(all_items)}",
        f"- Kinds: {dict(sorted(kind_counts.items()))}",
        f"- Roles: {dict(sorted(role_counts.items()))}",
        f"- Attributes: {dict(sorted(attr_counts.items()))}",
        f"- Decisions: {dict(sorted(decision_counts.items()))}",
        "",
    ]

    for path in source_files():
        relative = (
            path.relative_to(Path("/tmp/audit-work/candidate"))
            if path.is_relative_to(Path("/tmp/audit-work/candidate"))
            else path
        )
        file_items = [item for item in all_items if item["path"] == path]
        out.extend([f"## `{relative}`", ""])
        if not file_items:
            out.extend(["No local K declarations or rules.", ""])
            continue
        for item in file_items:
            item_decision, rationale = decision(item)
            attrs = ", ".join(item["attrs"]) or "none"
            out.extend(
                [
                    f"- L{item['line']} · {item['kind']} · {semantic_role(item)} "
                    f"· attrs: {attrs} · **{item_decision}**",
                    f"  - `{item['text']}`",
                    f"  - Decision basis: {rationale}.",
                ]
            )
        out.append("")

    OUTPUT.write_text("\n".join(out) + "\n")
    print(f"output={OUTPUT}")
    print(f"items={len(all_items)}")
    print(f"kinds={dict(sorted(kind_counts.items()))}")
    print(f"roles={dict(sorted(role_counts.items()))}")
    print(f"attributes={dict(sorted(attr_counts.items()))}")
    print(f"decisions={dict(sorted(decision_counts.items()))}")
    unresolved = [
        item
        for item in all_items
        if decision(item)[0] == "REVIEW"
    ]
    print(f"unresolved_candidate_local_items={len(unresolved)}")
    if unresolved:
        for item in unresolved:
            print(f"UNRESOLVED {item['path']}:{item['line']} {item['text']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
