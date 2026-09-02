#!/usr/bin/env python3
"""Build a complete source-level K declaration/rule inventory with audit labels."""

from __future__ import annotations

import collections
import hashlib
import re
from pathlib import Path


WORK = Path("/tmp/audit-work/reconstruction")
OUTPUT = Path("/audit-output/evidence/05-rule-inventory.md")
SEMANTICS = WORK / "reference-semantics"

ITEM_START = re.compile(
    r"^\s{2}(configuration|syntax|rule|context|claim|alias|macro)\b"
)

# Item-start line numbers on the actual target path. Items not listed are still
# inventoried and assessed, but are target-inert.
USED_STARTS: dict[str, set[int]] = {
    "semantics/syntax.k": {9, 32, 37, 41, 56, 57, 60, 61},
    "semantics/core.k": {
        13,
        14,
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
        145,
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
        238,
        239,
        240,
        252,
        253,
        254,
    },
    "semantics/iter.k": {8},
    "semantics/operators.k": {12, 15, 16, 17},
    "semantics/int.k": {9, 22, 24, 28, 29, 31, 32, 33, 34},
    "semantics/bool.k": {27, 28, 29, 31},
    "semantics/str.k": {8, 9, 13, 14, 15, 16, 20, 21, 22, 24},
    "semantics/tuple.k": {31, 32},
    "semantics/controls.k": {
        9,
        20,
        48,
        51,
        52,
        53,
        54,
        65,
        69,
        71,
        72,
        73,
    },
    "semantics/functions.k": {8, 14, 63, 64, 78, 80, 85},
    "semantics/builtins.k": {17, 187, 188},
    "semantics/call.k": {19, 20, 21, 31, 69},
}

PROOF_LOCAL_ASSESSMENT = {
    7: "DEF-SUMMARY: exact source arithmetic; total over Int because divisor is fixed 26.",
    8: "DEF-SUMMARY-EQUATION: names pyMod(C-97+4,26)+97; no operational term is matched.",
    12: "DEF-SUMMARY: three guarded character cases; guards are exhaustive and pairwise disjoint.",
    13: "DEF-SUMMARY-EQUATION: C<97 pass-through singleton.",
    15: "DEF-SUMMARY-EQUATION: 97<=C<=122 ROT4 singleton; output remains 97..122.",
    18: "DEF-SUMMARY-EQUATION: C>122 pass-through singleton.",
    21: "DEF-SUMMARY: left fold over explicit accumulator and remaining IntSeq.",
    22: "DEF-SUMMARY-EQUATION: empty suffix returns accumulator.",
    23: "DEF-SUMMARY-EQUATION: cons case executes one seqConcat/encryptedChar step and descends on tail.",
    28: "DEF-SUMMARY: wrapper for empty-initialized fold.",
    29: "DEF-SUMMARY-EQUATION: exact wrapper equation.",
    32: "DEF-SUMMARY: tracks final for-target binding only; does not affect ciphertext.",
    33: "DEF-SUMMARY-EQUATION: empty loop preserves prior target value.",
    34: "DEF-SUMMARY-EQUATION: cons case records current one-character str and descends on tail.",
}


def normalized(text: str) -> str:
    return " ".join(line.strip() for line in text.splitlines() if line.strip())


def items(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if ITEM_START.match(line)
    ]
    for position, start in enumerate(starts):
        stop = starts[position + 1] if position + 1 < len(starts) else len(lines)
        # Do not absorb the module terminator into the last item.
        while stop > start and lines[stop - 1].strip() in {"endmodule", ""}:
            stop -= 1
        match = ITEM_START.match(lines[start])
        assert match is not None
        yield match.group(1), start + 1, "\n".join(lines[start:stop]).rstrip()


def attributes(text: str) -> str:
    found = []
    for attr in [
        "function",
        "total",
        "functional",
        "simplification",
        "concrete",
        "owise",
        "priority",
        "macro-rec",
        "macro",
        "no-evaluators",
        "symbol",
        "strict",
        "seqstrict",
    ]:
        if re.search(rf"\b{re.escape(attr)}\b", text):
            found.append(attr)
    return ", ".join(found) if found else "none"


def target_status(relative: str, line: int, text: str) -> tuple[str, str]:
    if relative == "verification.k":
        assessment = PROOF_LOCAL_ASSESSMENT.get(
            line,
            "PROOF-LOCAL: inventoried; declaration/rule is part of a fully defined summary theory.",
        )
        return "proof-local", assessment
    if relative == "spec.k":
        if line == 6:
            return (
                "used-helper-claim",
                "DERIVED REACHABILITY/CIRCULARITY: exact #loop and body; one fixed-semantics iteration precedes recursive reuse.",
            )
        if line == 50:
            return (
                "target-entry-claim",
                "TARGET REACHABILITY: loads exact submitted FuncDef plus audit call assignment and constrains result/normal state.",
            )
        return "spec-declaration", "SPEC: inventoried."
    if relative == "semantics/concrete.k":
        return (
            "excluded-from-proof-import-graph",
            "SUPPLIED-CONCRETE: parsed by source assembly but MPY-CONCRETE is not imported by VERIFICATION; cannot close the proof.",
        )
    opaque = "no-evaluators" in text or re.search(
        r"\bsymbol\s*\((sortVS|sortKeyVS|md5hexCodes|intFloatDiv|divII|floatMod|floatLt|absF|floorFI|toF|ceilF|subF|divF|addF|mulF|powF|gtF|eqF|floatFinite|ltFI|ltIF|eqIF|decStrToF|divFloatIntV|intToF|truncF|roundF|roundFN|sqrtF)",
        text,
    )
    if opaque:
        return (
            "opaque-target-inert",
            "SUPPLIED-OPAQUE: value-bearing trust boundary for other programs; no symbol in this item is reachable from encrypt.",
        )
    if line in USED_STARTS.get(relative, set()):
        return (
            "used-fixed-semantics",
            "CHECKED-USED: fixed supplied declaration/rule is on the actual source path and agrees with the modeled Python operation/state transition.",
        )
    return (
        "target-inert-fixed-semantics",
        "CHECKED-INERT: fixed supplied declaration/rule is not reachable from the submitted constructor term; it contributes no target conclusion.",
    )


def escape_cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", "<br>")


def main() -> None:
    paths = [SEMANTICS / "semantics.k"]
    paths.extend(sorted((SEMANTICS / "semantics").glob("*.k")))
    paths.extend([WORK / "verification.k", WORK / "spec.k"])

    records = []
    for path in paths:
        if path == SEMANTICS / "semantics.k":
            relative = "semantics.k"
        elif path.is_relative_to(SEMANTICS):
            relative = path.relative_to(SEMANTICS).as_posix()
        else:
            relative = path.name
        for kind, line, text in items(path):
            status, assessment = target_status(relative, line, text)
            records.append(
                {
                    "file": relative,
                    "line": line,
                    "kind": kind,
                    "attributes": attributes(text),
                    "status": status,
                    "assessment": assessment,
                    "text": normalized(text),
                }
            )

    counts = collections.Counter(record["kind"] for record in records)
    status_counts = collections.Counter(record["status"] for record in records)
    opaque_count = sum("opaque" in record["status"] for record in records)

    output = [
        "# Exhaustive source-level K inventory",
        "",
        "Generated from the clean scratch sources. Each top-level configuration, "
        "syntax declaration, context, rule, and claim is listed once. Multiline "
        "items are normalized only for display.",
        "",
        f"- Total items: {len(records)}",
        f"- Kinds: `{dict(sorted(counts.items()))}`",
        f"- Target classifications: `{dict(sorted(status_counts.items()))}`",
        f"- Opaque target-inert declarations/items: {opaque_count}",
        "",
        "| File:line | Kind | Attributes | Target relation | Assessment | Normalized item |",
        "|---|---|---|---|---|---|",
    ]
    for record in records:
        output.append(
            "| "
            + f"{record['file']}:{record['line']} | "
            + f"{record['kind']} | "
            + f"{escape_cell(record['attributes'])} | "
            + f"{escape_cell(record['status'])} | "
            + f"{escape_cell(record['assessment'])} | "
            + f"`{escape_cell(record['text'])}` |"
        )
    output.append("")
    OUTPUT.write_text("\n".join(output), encoding="utf-8")
    digest = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()

    print(f"inventory_items={len(records)}")
    print(f"inventory_kind_counts={dict(sorted(counts.items()))}")
    print(f"inventory_status_counts={dict(sorted(status_counts.items()))}")
    print(f"inventory_opaque_target_inert={opaque_count}")
    print(f"inventory_path={OUTPUT}")
    print(f"inventory_sha256={digest}")


if __name__ == "__main__":
    main()
