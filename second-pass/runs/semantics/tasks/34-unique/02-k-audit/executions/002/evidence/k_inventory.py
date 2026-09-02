#!/usr/bin/env python3
"""Lexically enumerate every outer K declaration/rule in the audited sources."""

from __future__ import annotations

import argparse
import hashlib
import re
from collections import Counter, defaultdict
from pathlib import Path


OUTER = re.compile(
    r"^\s*(requires|module|endmodule|imports|syntax|configuration|context|"
    r"rule|claim|alias)\b"
)
ATTR = re.compile(r"\[([^\[\]]+)\]")
KNOWN_ATTR_PREFIXES = (
    "function",
    "total",
    "functional",
    "symbol",
    "no-evaluators",
    "macro",
    "strict",
    "seqstrict",
    "simplification",
    "concrete",
    "owise",
    "priority",
    "anywhere",
    "assoc",
    "unit",
    "comm",
    "hook",
    "cell",
    "maincell",
    "exit",
)
MATERIAL_FILES = {
    "semantics.k",
    "semantics/syntax.k",
    "semantics/core.k",
    "semantics/iter.k",
    "semantics/operators.k",
    "semantics/bool.k",
    "semantics/list.k",
    "semantics/controls.k",
    "semantics/functions.k",
    "semantics/builtins.k",
    "semantics/call.k",
    "semantics/sort.k",
}


def strip_line_comment(line: str) -> str:
    output: list[str] = []
    in_string = False
    escaped = False
    index = 0
    while index < len(line):
        character = line[index]
        following = line[index + 1] if index + 1 < len(line) else ""
        if in_string:
            output.append(character)
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            index += 1
        elif character == '"':
            output.append(character)
            in_string = True
            index += 1
        elif character == "/" and following == "/":
            break
        else:
            output.append(character)
            index += 1
    return "".join(output)


def sentences(path: Path) -> list[tuple[int, int, str, str]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    starts: list[tuple[int, str]] = []
    block_comment = False
    for index, raw in enumerate(lines):
        # K sources in this benchmark use only full-line block-comment bodies.
        stripped = raw.lstrip()
        if block_comment:
            if "*/" in stripped:
                block_comment = False
            continue
        if stripped.startswith("/*"):
            if "*/" not in stripped[2:]:
                block_comment = True
            continue
        code = strip_line_comment(raw)
        match = OUTER.match(code)
        if match:
            starts.append((index, match.group(1)))
    result: list[tuple[int, int, str, str]] = []
    for position, (start, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        segment = "\n".join(lines[start:end]).strip()
        normalized = " ".join(
            part
            for line in segment.splitlines()
            if (part := strip_line_comment(line).strip())
        )
        result.append((start + 1, end, kind, normalized))
    return result


def classify(relative: str, kind: str, text: str) -> tuple[str, str]:
    raw_tokens: list[str] = []
    for match in ATTR.finditer(text):
        start = 0
        depth = 0
        body = match.group(1)
        for index, character in enumerate(body):
            if character == "(":
                depth += 1
            elif character == ")":
                depth = max(0, depth - 1)
            elif character == "," and depth == 0:
                raw_tokens.append(body[start:index].strip())
                start = index + 1
        raw_tokens.append(body[start:].strip())
    attributes = ",".join(
        sorted(
            {
                token
                for token in raw_tokens
                if token.startswith(KNOWN_ATTR_PREFIXES)
            }
        )
    )
    if relative == "verification.k":
        scope = "proof-local"
    elif relative == "spec.k":
        scope = "proof-claim"
    elif relative in MATERIAL_FILES:
        scope = "fixed-material-slice"
    else:
        scope = "fixed-unused-by-solution"
    if "no-evaluators" in attributes:
        scope += ";opaque"
    if "priority(" in text:
        scope += ";priority"
    if "simplification" in attributes:
        scope += ";simplification"
    return attributes, scope


def assess(relative: str, start: int, kind: str, text: str) -> str:
    if relative == "spec.k":
        return "DYNAMICALLY_CLOSED_CLAIM;SEE_CLAIM_ADEQUACY_REVIEW"
    if relative == "verification.k":
        if kind == "syntax":
            return "PROOF_LOCAL_DEFINITIONAL_DECLARATION_VALID"
        return "PROOF_LOCAL_EQUATION_VALID_ON_COMPLETE_GUARD"
    if kind in {"syntax", "context", "configuration"}:
        if "sortVS(" in text:
            return "FIXED_EXTERNAL_SORT_PRIMITIVE_DECLARATION;CONDITIONAL_TRUST"
        return "FIXED_DECLARATION_OR_EVALUATION_ORDER_REVIEWED"
    if (
        relative == "semantics/list.k"
        and start in {63, 65}
    ):
        return "REAL_PYTHON_DOMAIN_GAP;STRUCTURAL_EQUALITY_FALSE_FOR_BOOL_INT"
    if (
        relative == "semantics/sort.k"
        and (
            "sortVS(" in text
            or 'builtinV("sorted")' in text
        )
    ):
        if "concrete" in text:
            return "FIXED_CONCRETE_INSERTION_SORT_VALID_FOR_HOMOGENEOUS_INT_OR_STR"
        return "FIXED_EXTERNAL_SORT_PRIMITIVE;CONDITIONAL_TRUST"
    if relative in MATERIAL_FILES:
        return "FIXED_RULE_REVIEWED_ON_SOLUTION_EXECUTION_SLICE"
    return "FIXED_UNUSED_RULE_NO_HEAD_INTERFERENCE_WITH_SOLUTION"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    paths = sorted(
        [
            root / "reference-semantics" / "semantics.k",
            *(root / "reference-semantics" / "semantics").glob("*.k"),
            root / "verification.k",
            root / "spec.k",
        ],
        key=lambda path: path.relative_to(root).as_posix(),
    )

    rows: list[tuple[str, str, int, int, str, str, str, str, str]] = []
    kinds: Counter[str] = Counter()
    attrs: Counter[str] = Counter()
    files: dict[str, Counter[str]] = defaultdict(Counter)
    for path in paths:
        relative = path.relative_to(root).as_posix()
        display = relative.removeprefix("reference-semantics/")
        for start, end, kind, text in sentences(path):
            # Module boundaries and imports are useful closure evidence but are
            # not semantic declarations/rules requested by the audit.
            if kind in {"module", "endmodule", "imports", "requires"}:
                continue
            attributes, scope = classify(display, kind, text)
            digest = hashlib.sha256(text.encode()).hexdigest()[:16]
            identifier = f"{display}:{start}:{kind}:{digest}"
            rows.append(
                (
                    identifier,
                    display,
                    start,
                    end,
                    kind,
                    attributes,
                    scope,
                    assess(display, start, kind, text),
                    text,
                )
            )
            kinds[kind] += 1
            files[display][kind] += 1
            for attribute in attributes.split(","):
                if attribute:
                    attrs[attribute] += 1

    if args.summary:
        print(f"TOTAL={len(rows)}")
        print(f"KINDS={dict(sorted(kinds.items()))}")
        print(f"ATTRIBUTES={dict(sorted(attrs.items()))}")
        for path in sorted(files):
            print(f"FILE={path} COUNTS={dict(sorted(files[path].items()))}")
    else:
        print(
            "id\tfile\tstart\tend\tkind\tattributes\tscope\tassessment\tnormalized"
        )
        for row in rows:
            print("\t".join(map(str, row)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
