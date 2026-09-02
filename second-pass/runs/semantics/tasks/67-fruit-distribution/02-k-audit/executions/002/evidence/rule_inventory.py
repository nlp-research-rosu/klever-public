#!/usr/bin/env python3
"""Inventory every declaration and rule in the fixed and proof-local K sources."""

from __future__ import annotations

from pathlib import Path
import re


FIXED_ROOT = Path("/reference/reference-semantics")
CANDIDATE_VERIFICATION = Path("/candidate/verification.k")
CANDIDATE_SPEC = Path("/candidate/spec.k")
DECLARATION = re.compile(
    r"^(configuration|syntax|context(?:\s+alias)?|rule|claim|module|endmodule|imports)\b"
)


# Lines on the actual target path, plus nearby dispatch rules that the
# proof-local bridges preempt. This is deliberately conservative.
USED_RANGES: dict[str, list[tuple[int, int]]] = {
    "semantics.k": [(34, 90)],
    "semantics/syntax.k": [(9, 15), (22, 22), (28, 30), (37, 41), (50, 61)],
    "semantics/core.k": [
        (13, 15), (25, 60), (68, 70), (117, 127), (130, 191),
        (194, 195), (208, 219), (223, 229),
    ],
    "semantics/controls.k": [(9, 18)],
    "semantics/functions.k": [(8, 20), (62, 90)],
    "semantics/call.k": [(15, 32), (47, 50), (69, 74)],
    "semantics/methods.k": [(70, 86)],
    "semantics/builtins.k": [(139, 160)],
    "semantics/subscript.k": [(6, 41)],
    "semantics/int.k": [(13, 13)],
    "semantics/operators.k": [(1, 47)],
    "semantics/str.k": [(12, 16)],
    "semantics/list.k": [(18, 20)],
}


def is_used(relative: str, line: int) -> bool:
    return any(start <= line <= end for start, end in USED_RANGES.get(relative, []))


def items(path: Path) -> list[tuple[int, str, str]]:
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        if line.startswith('requires "'):
            starts.append((index, "requires"))
            continue
        indent = len(line) - len(line.lstrip(" "))
        match = DECLARATION.match(line.lstrip(" ")) if indent <= 2 else None
        if match:
            starts.append((index, match.group(1)))
    result: list[tuple[int, str, str]] = []
    for position, (start, kind) in enumerate(starts):
        if kind in {"module", "endmodule", "imports", "requires"}:
            end = start + 1
        else:
            end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
            # Exclude comments and whitespace separating the next item, while
            # retaining guards, cells, continuation lines, and attributes.
            while end > start + 1 and (
                not lines[end - 1].strip()
                or lines[end - 1].lstrip().startswith("//")
            ):
                end -= 1
        text = " ".join(line.strip() for line in lines[start:end] if line.strip())
        text = re.sub(r"\s+", " ", text)
        result.append((start + 1, kind, text))
    return result


def attributes(text: str) -> str:
    labels = []
    for label, pattern in [
        ("function", r"\bfunction\b"),
        ("functional", r"\bfunctional\b"),
        ("total", r"\btotal\b"),
        ("no-evaluators", r"\bno-evaluators\b"),
        ("symbol", r"\bsymbol(?:\(|\b)"),
        ("concrete", r"\bconcrete\b"),
        ("simplification", r"\bsimplification\b"),
        ("owise", r"\bowise\b"),
        ("priority", r"\bpriority\("),
        ("macro", r"\bmacro\b"),
        ("strict", r"\b(?:seq)?strict(?:\(|\b)"),
    ]:
        if re.search(pattern, text):
            labels.append(label)
    return ", ".join(labels) if labels else "-"


def decision(path: Path, line: int, text: str) -> str:
    if path == CANDIDATE_VERIFICATION:
        if line == 9:
            return (
                "REJECT: two fresh opaque IntSeq constructors have no equations "
                "connecting them to ASCII decimal/sentence code sequences."
            )
        if line == 15:
            return (
                "REJECT: result-bearing operational split bridge fabricates five "
                "tokens from the same unconstrained constructors; no bridge-free "
                "connection theorem."
            )
        if line == 34:
            return (
                "REJECT: result-bearing int bridge maps the unconstrained "
                "decimalCodes(I) directly to I; no bridge-free connection theorem."
            )
        if line in {41, 42}:
            return (
                "ACCEPT: definitional program summary; independently regenerated "
                "constructor comparison is exact modulo optional .Exprs syntax."
            )
        return "ACCEPT: module plumbing only."
    if path == CANDIDATE_SPEC:
        if line == 6:
            return (
                "REJECT AS TARGET THEOREM: result-constraining and satisfiable, "
                "but its domain is the unconnected synthetic "
                "str(fruitSentenceCodes(A,B)), not actual source strings."
            )
        if line in {34, 56, 78, 100}:
            return (
                "ACCEPT AS FINITE GROUND FACT: concrete prompt example executes "
                "fixed split/int rules, but does not repair the general claim."
            )
        return "ACCEPT: module plumbing only."
    return (
        "ACCEPT AT SELECTED LEVEL: launcher-supplied fixed MPY semantics, "
        "byte-identical to the trusted mount; no candidate alteration."
    )


def main() -> int:
    paths = [FIXED_ROOT / "semantics.k"]
    paths.extend(sorted((FIXED_ROOT / "semantics").glob("*.k")))
    paths.append(CANDIDATE_VERIFICATION)
    paths.append(CANDIDATE_SPEC)

    rows = []
    kinds: dict[str, int] = {}
    opaque_rows = []
    for path in paths:
        relative = (
            str(path.relative_to(FIXED_ROOT))
            if path not in {CANDIDATE_VERIFICATION, CANDIDATE_SPEC}
            else (
                "candidate/verification.k"
                if path == CANDIDATE_VERIFICATION
                else "candidate/spec.k"
            )
        )
        for line, kind, text in items(path):
            kinds[kind] = kinds.get(kind, 0) + 1
            attrs = attributes(text)
            usage = "material/displaced" if (
                path in {CANDIDATE_VERIFICATION, CANDIDATE_SPEC}
                or is_used(relative, line)
            ) else "not reached by target"
            row = (relative, line, kind, attrs, usage, decision(path, line, text), text)
            rows.append(row)
            if "symbol" in attrs or (
                path == CANDIDATE_VERIFICATION and line == 9
            ):
                opaque_rows.append(row)

    out = Path("/audit-output/evidence/rule_inventory.md")
    with out.open("w") as stream:
        stream.write("# Exhaustive K source inventory\n\n")
        stream.write(
            "Generated from the trusted supplied-semantics tree and the "
            "candidate's proof-local `verification.k`. Multi-line declarations "
            "and rules are represented as one row.\n\n"
        )
        stream.write(f"Total inventoried items: {len(rows)}. Kinds: {kinds}.\n\n")
        stream.write(
            "| Source:line | Kind | Attributes | Target use | Decision | Exact item |\n"
        )
        stream.write("|---|---|---|---|---|---|\n")
        for relative, line, kind, attrs, usage, verdict, text in rows:
            safe = text.replace("|", "\\|")
            stream.write(
                f"| `{relative}:{line}` | {kind} | {attrs} | {usage} | "
                f"{verdict} | `{safe}` |\n"
            )
        stream.write("\n## Opaque/no-evaluator inventory\n\n")
        for relative, line, _kind, attrs, usage, verdict, text in opaque_rows:
            stream.write(
                f"- `{relative}:{line}` ({attrs}; {usage}): `{text}` — {verdict}\n"
            )

    print(f"inventory_path={out}")
    print(f"total_items={len(rows)}")
    print(f"kinds={kinds}")
    print(f"opaque_items={len(opaque_rows)}")
    print("candidate_rejected_items=3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
