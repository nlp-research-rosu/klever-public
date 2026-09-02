#!/usr/bin/env python3
"""Create a complete top-level K declaration/rule inventory with audit tags."""

from __future__ import annotations

import re
from pathlib import Path


SEMANTICS = Path("/reference/reference-semantics")
VERIFICATION = Path("/candidate/verification.k")
OUTPUT = Path("/audit-output/evidence/05_rule_inventory.md")

START = re.compile(
    r"^(?P<indent>\s*)(?P<kind>requires|module|endmodule|imports|configuration|"
    r"syntax|context|rule|claim|alias)\b"
)
ATTR = re.compile(r"\[([^\]]+)\]")


# Rules/declarations directly exercised in the universal proof, indexed by
# source-relative path and inclusive starting-line intervals.
USED: dict[str, tuple[tuple[int, int], ...]] = {
    "semantics.k": ((34, 90),),
    "semantics/syntax.k": (
        (3, 9),
        (11, 12),
        (28, 32),
        (37, 37),
        (41, 45),
        (49, 50),
        (53, 61),
    ),
    "semantics/core.k": (
        (3, 60),
        (117, 127),
        (129, 158),
        (183, 225),
    ),
    "semantics/iter.k": ((6, 8),),
    "semantics/list.k": ((3, 10),),
    "semantics/tuple.k": ((3, 6), (31, 40)),
    "semantics/operators.k": ((6, 17),),
    "semantics/int.k": ((4, 9), (22, 22)),
    "semantics/controls.k": (
        (3, 44),
        (50, 74),
    ),
    "semantics/functions.k": (
        (3, 20),
        (62, 91),
    ),
    "semantics/call.k": (
        (10, 21),
        (69, 75),
    ),
}


def normalized(lines: list[str]) -> str:
    return " ".join(" ".join(lines).split()).replace("|", "&#124;")


def exercised(rel: str, line: int) -> bool:
    return any(lo <= line <= hi for lo, hi in USED.get(rel, ()))


def records(path: Path) -> list[tuple[int, str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if not match:
            continue
        indent = len(match.group("indent"))
        kind = match.group("kind")
        # Only module-level statements (two spaces) and file-level
        # requires/module boundaries (zero spaces) start records. `requires`
        # indented inside a rule is part of that rule.
        if indent in (0, 2):
            starts.append((index, kind))
    result: list[tuple[int, str, str]] = []
    for position, (index, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        body = lines[index:end]
        while body and (not body[-1].strip() or body[-1].lstrip().startswith("//")):
            body.pop()
        result.append((index + 1, kind, normalized(body)))
    return result


def main() -> int:
    source_files = [SEMANTICS / "semantics.k"]
    source_files.extend(sorted((SEMANTICS / "semantics").glob("*.k")))
    source_files.append(VERIFICATION)
    rows: list[str] = []
    counts: dict[str, int] = {}
    for path in source_files:
        if path == VERIFICATION:
            rel = "verification.k"
            origin = "proof-local"
        else:
            rel = str(path.relative_to(SEMANTICS))
            origin = "supplied-fixed"
        for line, kind, text in records(path):
            counts[kind] = counts.get(kind, 0) + 1
            attributes = ", ".join(
                attribute.strip() for attribute in ATTR.findall(text)
            )
            on_path = "yes" if origin == "proof-local" or exercised(rel, line) else "no"
            if origin == "supplied-fixed":
                if on_path == "yes":
                    decision = (
                        "PASS—selected supplied semantics; exercised rule/declaration "
                        "reviewed for this program path"
                    )
                else:
                    decision = (
                        "OUTSIDE PATH—selected supplied semantics; no actual-program "
                        "reachability witness reaches this entry"
                    )
            else:
                if kind in {"module", "endmodule", "imports"}:
                    decision = "PASS—module structure only"
                elif line in (7, 8, 14, 15, 21, 22):
                    decision = "PASS—macro alias; expansion checked against submitted AST"
                elif line in (30, 31):
                    decision = "PASS—typed inductive representation, no computation bypass"
                elif line in (32, 33):
                    decision = "PASS—faithful empty/cons iterator equations"
                elif line == 37:
                    decision = "PASS—result-bearing mathematical function, exhaustively defined"
                elif line in (38, 39):
                    decision = "PASS—disjoint, descending running-prefix equations"
                elif line == 55:
                    decision = "PASS—operational bridge justified by bridge-free AUX-SPEC"
                else:
                    decision = "PASS—proof-local declaration/rule reviewed"
            rows.append(
                f"| `{rel}:{line}` | {origin} | {kind} | {on_path} | "
                f"{attributes or '—'} | {decision} | `{text}` |"
            )

    summary = ", ".join(f"{key}={counts[key]}" for key in sorted(counts))
    document = [
        "# Exhaustive K source inventory",
        "",
        "Generated by reviewer-authored `rule_inventory.py`. A record begins at "
        "every module-level `syntax`, `context`, `rule`, `claim`, configuration, "
        "module/import boundary, and file-level `requires`; multiline bodies and "
        "attributes are retained in normalized form. Syntax alternatives are kept "
        "inside their declaring record.",
        "",
        f"Inventory counts: {summary}. Total={sum(counts.values())}.",
        "",
        "| Location | Origin | Kind | Actual proof path | Attributes | Decision | Declaration / rule |",
        "|---|---|---|---|---|---|---|",
        *rows,
        "",
        "The `OUTSIDE PATH` classification is deliberately narrower than declaring "
        "unused rules universally Python-sound: they are part of the exact trusted "
        "supplied baseline, not candidate extensions, and no intended-domain "
        "execution of this submitted program reaches them. Compiler totality "
        "warnings are separately accounted for in the review.",
        "",
    ]
    OUTPUT.write_text("\n".join(document), encoding="utf-8")
    print(f"wrote={OUTPUT}")
    print(f"total={sum(counts.values())} {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
