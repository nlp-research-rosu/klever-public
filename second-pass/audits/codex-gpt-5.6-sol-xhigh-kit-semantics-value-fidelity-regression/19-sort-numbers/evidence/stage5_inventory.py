#!/usr/bin/env python3
"""Produce a source-level inventory of all K declarations, rules, and claims."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path


START = re.compile(r"^\s*(configuration|syntax|rule|claim|context|alias)\b")
BOUNDARY = re.compile(
    r"^\s*(configuration|syntax|rule|claim|context|alias|module|endmodule)\b"
)


def source_units(path: Path) -> list[tuple[int, str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if START.match(line) and not line.lstrip().startswith("//")
    ]
    units: list[tuple[int, str, str]] = []
    for start_position, start in enumerate(starts):
        match = START.match(lines[start])
        assert match is not None
        kind = match.group(1)
        end = len(lines)
        for later in starts[start_position + 1 :]:
            if BOUNDARY.match(lines[later]):
                end = later
                break
        block = lines[start:end]
        while block and (not block[-1].strip() or block[-1].lstrip().startswith("//")):
            block.pop()
        units.append((start + 1, kind, "\n".join(block)))
    return units


def attributes(text: str) -> list[str]:
    names = (
        "function",
        "total",
        "functional",
        "simplification",
        "concrete",
        "owise",
        "no-evaluators",
        "macro",
    )
    result = [name for name in names if re.search(rf"\b{re.escape(name)}\b", text)]
    if "priority(" in text:
        result.append("priority")
    if "symbol(" in text:
        result.append("symbol")
    return result


def subtype(kind: str, text: str) -> str:
    attrs = attributes(text)
    if kind == "syntax":
        if "no-evaluators" in attrs:
            return "opaque-symbol-declaration"
        if "symbol" in attrs:
            return "symbol-declaration"
        if "function" in attrs or "functional" in attrs:
            return "function-declaration"
        return "syntax-declaration"
    if kind == "rule":
        if "simplification" in attrs:
            return "simplification-rule"
        if "priority" in attrs:
            return "priority-semantic-rule"
        if "<k>" in text or re.search(r"<[A-Za-z][^>]*>", text):
            return "ordinary-semantic-rule"
        return "equational-rule"
    return kind


REACHABLE = {
    "syntax.k": ("Module(", "FuncDef", "Params", "If", "Compare", "Name", "CmpOp",
                 "Str", "Return", "Int", "Call", "Attribute", "KwArg"),
    "core.k": ("#loadAll", "#look", "builtinsScope", "#evalArgs", "#evalArgCont",
               "#applyK", "#alloc", "#kwTag", "Int(", "appendVal", "truthy"),
    "operators.k": ("Compare(", "applyCmp"),
    "str.k": ("Str(", "strToCodes", 'applyCmp("=="'),
    "controls.k": ("If(", "#branch"),
    "functions.k": ("FuncDef(", "#bindP", "Return(", "#endcall", "#pop", "frame("),
    "call.k": ("Attribute(", "Call(", "#callee", "#applyK", "closureVal(",
               "isMutMethod"),
    "methods.k": ('"join"', "joinCodes", '"split"', "splitWS", "flushTok", "isWSC"),
    "sort.k": ('builtinV("sorted")', "sortKeyVS"),
    "concrete.k": ("#ksort", "#ksIns", "insPair", "kLt", "unpairVS",
                   'builtinV("sorted")'),
}


def disposition(path: Path, kind: str, text: str) -> str:
    if path.name == "verification.k":
        return "PROOF_LOCAL_MANUAL_REVIEW_PASS"
    if path.name == "spec.k":
        return "CLAIM_MANUAL_REVIEW_PASS"
    if "no-evaluators" in attributes(text):
        if "sortKeyVS" in text:
            return "REACHABLE_TRUSTED_OPAQUE_PRIMITIVE"
        return "UNUSED_TRUSTED_OPAQUE_PRIMITIVE"
    keywords = REACHABLE.get(path.name, ())
    if keywords and any(keyword in text for keyword in keywords):
        if path.name == "concrete.k":
            return "CONCRETE_EMPIRICAL_BRIDGE_MANUAL_REVIEW_PASS"
        return "REACHABLE_FIXED_SEMANTICS_MANUAL_REVIEW_PASS"
    return "OUTSIDE_REACHABLE_SLICE_NO_INTENDED_DOMAIN_WITNESS"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()

    files = [arguments.root / "reference-semantics" / "semantics.k"]
    files += sorted((arguments.root / "reference-semantics" / "semantics").glob("*.k"))
    files += [arguments.root / "verification.k", arguments.root / "spec.k"]

    units: list[tuple[Path, int, str, str, str, list[str], str]] = []
    counts: Counter[str] = Counter()
    disposition_counts: Counter[str] = Counter()
    for path in files:
        for line, kind, text in source_units(path):
            unit_subtype = subtype(kind, text)
            unit_attributes = attributes(text)
            unit_disposition = disposition(path, kind, text)
            counts[unit_subtype] += 1
            disposition_counts[unit_disposition] += 1
            units.append(
                (
                    path,
                    line,
                    kind,
                    unit_subtype,
                    text,
                    unit_attributes,
                    unit_disposition,
                )
            )

    with arguments.output.open("w", encoding="utf-8") as output:
        output.write("# Exhaustive K source inventory\n\n")
        output.write(
            "This mechanically enumerates every `configuration`, `syntax`, "
            "`rule`, `claim`, `context`, and `alias` source unit in the clean "
            "scratch inputs. Dispositions are audit classifications, not K "
            "attributes. An outside-slice disposition means only that the real "
            "submitted program cannot reach the unit on the intended domain; "
            "it is not a global soundness endorsement.\n\n"
        )
        output.write("## Counts\n\n")
        for name, count in sorted(counts.items()):
            output.write(f"- {name}: {count}\n")
        output.write("\n## Disposition counts\n\n")
        for name, count in sorted(disposition_counts.items()):
            output.write(f"- {name}: {count}\n")
        output.write("\n## Units\n\n")
        for path, line, kind, unit_subtype, text, unit_attributes, unit_disposition in units:
            relative = path.relative_to(arguments.root)
            output.write(f"### `{relative}:{line}`\n\n")
            output.write(f"- Kind: `{kind}` / `{unit_subtype}`\n")
            output.write(
                "- Attributes: "
                + (", ".join(f"`{name}`" for name in unit_attributes) or "none")
                + "\n"
            )
            output.write(f"- Disposition: `{unit_disposition}`\n\n")
            output.write("```k\n")
            output.write(text)
            output.write("\n```\n\n")

    print(f"FILES={len(files)}")
    print(f"UNITS={len(units)}")
    for name, count in sorted(counts.items()):
        print(f"COUNT_{name.upper().replace('-', '_')}={count}")
    for name, count in sorted(disposition_counts.items()):
        print(f"DISPOSITION_{name}={count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
