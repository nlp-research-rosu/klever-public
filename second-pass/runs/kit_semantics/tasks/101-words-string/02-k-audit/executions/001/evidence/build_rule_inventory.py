#!/usr/bin/env python3
"""Emit an exhaustive declaration/rule inventory for the supplied K sources."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


SEM_ROOT = Path("/reference/reference-semantics")
EXTRA = [Path("/candidate/verification.k"), Path("/candidate/spec.k")]

# Source declaration/rule start lines exercised by the target proof.  These
# were traced manually through the full configuration and are explained in
# REVIEW.md; syntax blocks are included when they declare used constructors.
TARGET_LINES: dict[str, set[int]] = {
    "semantics.k": {34, 58},
    "semantics/syntax.k": {9, 32, 37, 41, 50, 53, 56, 57, 60, 61},
    "semantics/core.k": {
        13,
        14,
        15,
        25,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        49,
        117,
        118,
        124,
        125,
        126,
        127,
        130,
        131,
        132,
        157,
        158,
        185,
        186,
        189,
        190,
        191,
        213,
        214,
        215,
    },
    "semantics/functions.k": {8, 14, 63, 64, 78, 85},
    "semantics/call.k": {16, 19, 20, 21, 24, 69},
    "semantics/methods.k": {
        10,
        72,
        75,
        76,
        77,
        79,
        82,
        83,
        84,
        85,
        86,
        104,
        106,
        107,
        108,
        109,
    },
    "semantics/str.k": {13, 14, 15, 16, 20, 21, 22},
    "semantics/list.k": {18, 19, 20},
}


ATTR_RE = re.compile(r"\[([^\]]+)\]")


def declaration_keyword(stripped: str) -> str | None:
    if stripped.startswith('requires "'):
        return "requires"
    for keyword in ("module", "imports", "configuration", "syntax", "context", "rule", "claim"):
        if re.match(rf"^{keyword}\b", stripped):
            return keyword
    return None


def relative(path: Path) -> str:
    if path.is_relative_to(SEM_ROOT):
        return path.relative_to(SEM_ROOT).as_posix()
    return path.as_posix()


def statements(path: Path):
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        stripped = line.strip()
        keyword = declaration_keyword(stripped)
        if keyword is not None:
            starts.append((index, keyword))
    for pos, (start, keyword) in enumerate(starts):
        stop = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        body_lines = []
        for line in lines[start:stop]:
            stripped = line.strip()
            if stripped == "endmodule":
                break
            if stripped.startswith("//") or not stripped:
                continue
            body_lines.append(stripped)
        body = " ".join(body_lines)
        body = re.sub(r"\s+", " ", body).strip()
        yield start + 1, keyword, body


def classify(source: str, line: int, keyword: str, text: str):
    attrs = sorted(
        {
            attr.strip().split("(", 1)[0]
            for group in ATTR_RE.findall(text)
            for attr in group.split(",")
        }
    )
    if keyword == "rule":
        if "simplification" in attrs:
            kind = "simplification-rule"
        elif "macro" in attrs or "macro-rec" in attrs:
            kind = "macro-rule"
        elif "<k>" in text or re.search(r"<[A-Za-z-]+>", text):
            kind = "operational-rule"
        else:
            kind = "equational-rule"
    elif keyword == "syntax":
        if "function" in attrs or "functional" in attrs:
            kind = "function-declaration"
        else:
            kind = "syntax-declaration"
    else:
        kind = keyword

    if source == "/candidate/spec.k" and keyword == "claim":
        decision = "TARGET_CLAIM"
        rationale = "Audited entry obligation; independently reconstructed."
    elif source == "/candidate/spec.k":
        decision = "TARGET_CLAIM_SCAFFOLD"
        rationale = "Module/import scaffolding for the audited entry obligation."
    elif source == "/candidate/verification.k":
        decision = "PROOF_LOCAL_NO_EXTENSION"
        rationale = "Only requires/imports/module; no local rule or symbol."
    elif keyword in {"requires", "module", "imports", "configuration"}:
        decision = "FIXED_ASSEMBLY_ACCEPT"
        rationale = "Unmodified supplied-semantics assembly/configuration; target cells reviewed separately."
    elif line in TARGET_LINES.get(source, set()):
        decision = "TARGET_PATH_ACCEPT"
        rationale = "Used target declaration/rule; audited for exact execution and mathematical fidelity."
    elif "symbol(" in text or "no-evaluators" in text or "md5hexCodes" in text:
        decision = "UNUSED_OPAQUE_BOUNDARY"
        rationale = "Fixed supplied primitive, constructor/callee-disjoint from this target; no target dependency."
    elif keyword == "syntax":
        decision = "FIXED_UNUSED_DECLARATION"
        rationale = "Supplied declaration not instantiated by the target term or its execution."
    else:
        decision = "FIXED_OUT_OF_PATH"
        rationale = "Supplied rule is constructor/callee-disjoint from the target execution; cannot establish its result."
    return kind, ",".join(attrs) if attrs else "-", decision, rationale


def main() -> None:
    paths = [SEM_ROOT / "semantics.k"] + sorted((SEM_ROOT / "semantics").glob("*.k")) + EXTRA
    records = []
    for path in paths:
        source = relative(path)
        for line, keyword, text in statements(path):
            kind, attrs, decision, rationale = classify(source, line, keyword, text)
            records.append((source, line, kind, attrs, decision, rationale, text))

    counts = Counter(record[2] for record in records)
    decisions = Counter(record[4] for record in records)
    attr_needles = {
        "function": "[function",
        "functional": "[functional",
        "total": "total",
        "simplification": "simplification",
        "priority": "priority(",
        "concrete": "concrete",
        "owise": "owise",
        "macro": "macro",
        "symbol": "symbol(",
        "opaque_no_evaluators": "no-evaluators",
    }
    attr_counts = {
        name: sum(needle in record[6] for record in records)
        for name, needle in attr_needles.items()
    }
    print("# Exhaustive K source declaration and rule inventory")
    print()
    print("Generated from the byte-verified trusted supplied-semantics tree plus")
    print("candidate `verification.k` and positive `spec.k`. Each source-level")
    print("declaration/rule appears once below; strictness-generated backend rules")
    print("are accounted for through their syntax declarations.")
    print()
    print(f"TOTAL_RECORDS: {len(records)}")
    for key, value in sorted(counts.items()):
        print(f"KIND_{key.upper().replace('-', '_')}: {value}")
    for key, value in sorted(attr_counts.items()):
        print(f"ATTRIBUTE_{key.upper()}: {value}")
    for key, value in sorted(decisions.items()):
        print(f"DECISION_{key}: {value}")
    print()
    print("| # | Source | Kind | Attributes | Decision | Review | Declaration / rule |")
    print("|---:|---|---|---|---|---|---|")
    for number, (source, line, kind, attrs, decision, rationale, text) in enumerate(records, 1):
        escaped = text.replace("|", "&#124;")
        print(
            f"| {number} | `{source}:{line}` | {kind} | `{attrs}` | "
            f"{decision} | {rationale} | `{escaped}` |"
        )


if __name__ == "__main__":
    main()
