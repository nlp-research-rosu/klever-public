#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


SENTENCE = re.compile(
    r"^[ \t]{2}(imports|syntax|configuration|context|rule|claim|alias)\b"
)
MODULE = re.compile(r"^[ \t]*module[ \t]+([A-Za-z][A-Za-z0-9_-]*)\b")
ENDMODULE = re.compile(r"^[ \t]*endmodule\b")
ATTRIBUTES = re.compile(r"\[([^\[\]\n]*)\]")
ATTRIBUTE_MARKERS = re.compile(
    r"\b(function|total|functional|symbol|no-evaluators|priority|"
    r"simplification|owise|concrete|macro|macro-rec|strict|seqstrict|"
    r"label|heat|cool|exit)\b"
)


@dataclass
class Item:
    source: str
    module: str
    line_start: int
    line_end: int
    keyword: str
    category: str
    attributes: str
    relevance: str
    decision: str
    digest: str
    normalized: str


USED_STARTS: dict[str, set[int]] = {
    "semantics/syntax.k": {9, 32, 41, 56, 57, 60, 61},
    "semantics/core.k": {
        13, 14, 15, 25, 36, 37, 38, 39, 40, 41, 42, 49,
        68, 75, 76, 85, 92, 100, 104, 106, 107, 109, 113,
        117, 124, 125, 126, 127, 130, 131, 132, 152, 157, 158,
        185, 186, 189, 190, 191, 194, 199, 200, 202, 208, 209,
        210, 213, 214, 215,
    },
    "semantics/operators.k": {10, 12, 15, 16, 17},
    "semantics/int.k": {7, 13, 15, 19, 20, 27},
    "semantics/str.k": {13, 14, 15, 16},
    "semantics/controls.k": {
        9, 20, 48, 65, 77, 78, 79, 81, 85,
    },
    "semantics/functions.k": {
        8, 14, 62, 63, 64, 77, 78, 80, 85,
    },
    "semantics/call.k": {19, 20, 21, 69},
}


def mask_comments(text: str) -> str:
    output = list(text)
    index = 0
    state = "code"
    depth = 0
    while index < len(text):
        current = text[index]
        following = text[index + 1] if index + 1 < len(text) else ""
        if state == "line":
            if current == "\n":
                state = "code"
            else:
                output[index] = " "
            index += 1
            continue
        if state == "block":
            if current == "/" and following == "*":
                output[index] = output[index + 1] = " "
                depth += 1
                index += 2
            elif current == "*" and following == "/":
                output[index] = output[index + 1] = " "
                depth -= 1
                index += 2
                if depth == 0:
                    state = "code"
            else:
                if current != "\n":
                    output[index] = " "
                index += 1
            continue
        if state == "string":
            if current == "\\" and following:
                index += 2
            else:
                if current == '"':
                    state = "code"
                index += 1
            continue
        if current == "/" and following == "/":
            output[index] = output[index + 1] = " "
            state = "line"
            index += 2
        elif current == "/" and following == "*":
            output[index] = output[index + 1] = " "
            state = "block"
            depth = 1
            index += 2
        else:
            if current == '"':
                state = "string"
            index += 1
    return "".join(output)


def category(keyword: str, normalized: str, attributes: list[str]) -> str:
    joined = ",".join(attributes)
    if keyword == "syntax":
        flags = []
        if "function" in joined:
            flags.append("function")
        if "total" in joined:
            flags.append("total")
        if "functional" in joined:
            flags.append("functional")
        if "no-evaluators" in joined:
            flags.append("opaque")
        if "macro" in joined:
            flags.append("macro")
        return "syntax" + (":" + "+".join(flags) if flags else "")
    if keyword == "rule":
        flags = []
        if "simplification" in joined:
            flags.append("simplification")
        if "priority" in joined:
            flags.append("priority")
        if "concrete" in joined:
            flags.append("concrete")
        if "owise" in joined:
            flags.append("owise")
        if "macro" in joined:
            flags.append("macro")
        return "rule" + (":" + "+".join(flags) if flags else ":ordinary")
    return keyword


def classify(source: str, line_start: int, keyword: str, category_name: str) -> tuple[str, str]:
    if source == "verification.k":
        if line_start == 8:
            return "proof-local", "exact syntactic sharing; sound"
        if line_start in {22, 23}:
            return "proof-local", "mathematical summary declaration; sound"
        if line_start == 9:
            return "proof-local", "exact regenerated statement body; sound"
        if line_start == 25:
            return "proof-local-unused", "truthful definition; unused by target claims"
        if line_start == 28:
            return "proof-local", "divisor base equation; sound on guard"
        if line_start == 31:
            return "proof-local", "descending non-divisor equation; sound and decreasing"
        if line_start == 38:
            return "proof-local", "guarded extensional Map deletion fact; sound"
        return "proof-local", "declaration/import; no execution shortcut"
    if source == "spec.k":
        return "target-claim", "audited separately for adequacy and satisfiability"
    if source == "semantics.k":
        return "assembly", "module assembly only"
    if source == "semantics/concrete.k":
        return (
            "concrete-only",
            "excluded from Haskell proof definition; checked only by fresh krun",
        )
    if line_start in USED_STARTS.get(source, set()):
        return (
            "reachable",
            "fixed supplied rule/declaration; reviewed sound on submitted integer path",
        )
    if ":opaque" in category_name:
        return (
            "unreachable-opaque",
            "fixed supplied trust boundary; unreachable from submitted program",
        )
    return (
        "unreachable",
        "constructor/type/context cannot arise on submitted program; no theorem influence",
    )


def parse_file(path: Path, label: str) -> list[Item]:
    text = path.read_text()
    masked = mask_comments(text)
    raw_lines = text.splitlines()
    masked_lines = masked.splitlines()
    module = ""
    starts: list[tuple[int, str, str]] = []
    for number, line in enumerate(masked_lines, 1):
        module_match = MODULE.match(line)
        if module_match:
            module = module_match.group(1)
            continue
        if ENDMODULE.match(line):
            module = ""
            continue
        sentence_match = SENTENCE.match(line)
        if module and sentence_match:
            starts.append((number, sentence_match.group(1), module))

    items: list[Item] = []
    for index, (start, keyword, module_name) in enumerate(starts):
        next_start = starts[index + 1][0] if index + 1 < len(starts) else len(raw_lines) + 1
        end = next_start - 1
        for probe in range(start, next_start):
            if probe - 1 < len(masked_lines) and ENDMODULE.match(masked_lines[probe - 1]):
                end = probe - 1
                break
            if (
                probe != start
                and probe - 1 < len(masked_lines)
                and MODULE.match(masked_lines[probe - 1])
            ):
                end = probe - 1
                break
        segment = "\n".join(raw_lines[start - 1 : end])
        normalized = " ".join(mask_comments(segment).split())
        attrs = [
            value.strip()
            for value in ATTRIBUTES.findall(mask_comments(segment))
            if value.strip() and ATTRIBUTE_MARKERS.search(value)
        ]
        category_name = category(keyword, normalized, attrs)
        relevance, decision = classify(
            label, start, keyword, category_name
        )
        items.append(
            Item(
                source=label,
                module=module_name,
                line_start=start,
                line_end=end,
                keyword=keyword,
                category=category_name,
                attributes=" | ".join(attrs),
                relevance=relevance,
                decision=decision,
                digest=hashlib.sha256(normalized.encode()).hexdigest(),
                normalized=normalized,
            )
        )
    return items


def clean(value: str) -> str:
    return value.replace("\t", " ").replace("\r", " ").replace("\n", " ")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    semantics_root = Path("/reference/reference-semantics")
    paths = [semantics_root / "semantics.k"] + sorted(
        (semantics_root / "semantics").glob("*.k")
    )
    labeled = [
        (path, path.relative_to(semantics_root).as_posix()) for path in paths
    ]
    labeled += [
        (Path("/candidate/verification.k"), "verification.k"),
        (Path("/candidate/spec.k"), "spec.k"),
    ]

    inventory: list[Item] = []
    for path, label in labeled:
        inventory.extend(parse_file(path, label))

    header = [
        "id", "source", "module", "line_start", "line_end", "keyword",
        "category", "attributes", "relevance", "decision", "normalized_sha256",
        "normalized_sentence",
    ]
    rows = ["\t".join(header)]
    for number, item in enumerate(inventory, 1):
        values = [
            f"K-{number:04d}",
            item.source,
            item.module,
            str(item.line_start),
            str(item.line_end),
            item.keyword,
            item.category,
            item.attributes,
            item.relevance,
            item.decision,
            item.digest,
            item.normalized,
        ]
        rows.append("\t".join(clean(value) for value in values))
    args.output.write_text("\n".join(rows) + "\n")

    categories = Counter(item.category for item in inventory)
    relevance = Counter(item.relevance for item in inventory)
    sources = Counter(item.source for item in inventory)
    print(f"inventory_path={args.output}")
    print(f"inventory_items={len(inventory)}")
    print(f"source_counts={dict(sorted(sources.items()))}")
    print(f"category_counts={dict(sorted(categories.items()))}")
    print(f"relevance_counts={dict(sorted(relevance.items()))}")
    print(
        "functional_declaration_count="
        f"{sum('functional' in item.category for item in inventory)}"
    )
    print(
        "opaque_declaration_count="
        f"{sum('opaque' in item.category for item in inventory)}"
    )
    print(
        "simplification_rule_count="
        f"{sum('simplification' in item.category for item in inventory)}"
    )
    print(
        "priority_rule_count="
        f"{sum('priority' in item.category for item in inventory)}"
    )


if __name__ == "__main__":
    main()
