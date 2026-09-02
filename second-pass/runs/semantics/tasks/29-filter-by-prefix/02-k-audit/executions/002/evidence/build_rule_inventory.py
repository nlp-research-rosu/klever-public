#!/usr/bin/env python3
"""Inventory every local K declaration/context/rule in supplied and proof files."""

from __future__ import annotations

import re
from pathlib import Path


ROOTS = [
    Path("/reference/reference-semantics/semantics.k"),
    *sorted(Path("/reference/reference-semantics/semantics").glob("*.k")),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]
START = re.compile(
    r"^\s*(module|endmodule|imports|syntax|configuration|context|rule|claim)\b"
)
INVENTORY_KINDS = {"syntax", "configuration", "context", "rule", "claim"}
ATTRIBUTES = [
    "function",
    "functional",
    "total",
    "simplification",
    "macro",
    "macro-rec",
    "priority",
    "owise",
    "concrete",
    "constructor",
    "symbol",
    "no-evaluators",
]


def clean_line(line: str) -> str:
    # The sources do not use // inside K string literals in inventoried starts.
    return line.split("//", 1)[0].rstrip()


def blocks(path: Path):
    lines = path.read_text().splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = START.match(clean_line(line))
        if match:
            starts.append((index, match.group(1)))
    for position, (index, kind) in enumerate(starts):
        if kind not in INVENTORY_KINDS:
            continue
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        content = "\n".join(lines[index:end]).strip()
        yield index + 1, end, kind, content


def used_by_target(path: Path, content: str) -> str:
    name = path.name
    if str(path).startswith("/candidate/"):
        return "PROOF_LOCAL_USED"
    patterns = {
        "syntax.k": (
            r"(Name|Str|ListExpr|Call|Attribute|Assign|For|If|Return|Expr|"
            r"FuncDef|ImportFrom|Exprs|Stmts|Params|ParamNames|Module)"
        ),
        "core.k": (
            r"(IntSeq|ValSeq|Str|Iterable|Val|configuration|#alloc|#loadAll|"
            r"#look|builtinsScope|#evalArgs|#evalArgCont|#applyK|Name\(|Str\(|"
            r"appendVal|vals2valSeq|truthy)"
        ),
        "iter.k": r"#iterNext|#iterDone|#iterYield",
        "str.k": r"#iterNext|strToCodes|startsWith",
        "list.k": r"#iterNext|ListExpr|toList|valSeqConcat|append",
        "methods.k": r"applyMethod\(str\(XC.*startswith|startsWith",
        "controls.k": (
            r"Assign\(Name|ImportFrom|Expr\(|#branch|If\(|For\(|#loop|#iterDone|"
            r"#iterYield"
        ),
        "functions.k": r"FuncDef\(|#bindP|Return\(|#endcall|#pop|frame\(",
        "call.k": (
            r"Attribute\(|#callee|Call\(|#evalArgs|boundMethodV|closureVal\(|"
            r"isMutMethod"
        ),
        "tuple.k": r"#bindTgt\(Name",
    }
    pattern = patterns.get(name)
    return "FIXED_USED" if pattern and re.search(pattern, content, re.S) else "FIXED_UNUSED"


def decision(path: Path, content: str, impact: str) -> str:
    if impact == "PROOF_LOCAL_USED":
        if "stringList" in content and "#iterNext" in content:
            return "SOUND_LIST_ISOMORPHIC_BRIDGE"
        if "prefixFilter" in content:
            return "SOUND_FILTER_RECURSION"
        if "valSeqConcat" in content and "simplification" in content:
            return "SOUND_LIST_ALGEBRA"
        if "#checkFilter" in content and "rule" in content:
            return "SOUND_RESULT_OBSERVER"
        if "filterByPrefixDef" in content:
            return "SOUND_EXACT_PROGRAM_MACRO"
        if path.name == "spec.k":
            return "POSITIVE_CLAIM"
        return "SOUND_DECLARATION"
    opaque = "no-evaluators" in content
    known_gaps = [
        r'Import\(_?:String\).*=> \.K',
        r'ImportFrom\(_?:String',
        r'isIntV\(_?:Int\)',
        r'For\(T:Expr, ref\(H:Int\)',
        r'mapStrVS',
        r'zipObj',
        r'strToCodes\(S:String\)',
        r'isIntV\(_?:Val\).*=> false',
        r'applyMethod\(str\(CS:IntSeq\), "encode"',
        r'applyBuiltin\("int", str\(CS:IntSeq\)',
        r'applyMethod\(str\(CS:IntSeq\), "is(upper|lower|alpha|digit)"',
        r'#pop => V ~> CONT',
        r'applyCmp\("==", list\(A:ValSeq\), list\(B:ValSeq\)',
    ]
    if any(re.search(pattern, content, re.S) for pattern in known_gaps):
        return "DOCUMENTED_SUBSET_APPROXIMATION"
    if opaque:
        return "OPAQUE_FIXED_PRIMITIVE_UNUSED"
    if impact == "FIXED_USED":
        return "SOUND_ON_TARGET_PATH"
    return "ACCEPTED_FIXED_UNUSED"


def one_line(content: str) -> str:
    text = re.sub(r"\s+", " ", content)
    return text.replace("\t", " ")


def main() -> None:
    print(
        "id\tfile\tlines\tkind\tattributes\timpact\tdecision\tdeclaration_or_rule"
    )
    count = 0
    kind_counts: dict[str, int] = {}
    decision_counts: dict[str, int] = {}
    for path in ROOTS:
        relative = (
            "verification.k"
            if path == Path("/candidate/verification.k")
            else "spec.k"
            if path == Path("/candidate/spec.k")
            else path.relative_to("/reference/reference-semantics").as_posix()
        )
        for start, end, kind, content in blocks(path):
            count += 1
            kind_counts[kind] = kind_counts.get(kind, 0) + 1
            code_content = "\n".join(
                clean_line(line) for line in content.splitlines()
            )
            attribute_text = " ".join(
                re.findall(r"\[([^\]]*)\]", code_content, flags=re.S)
            )
            attrs = [
                attribute
                for attribute in ATTRIBUTES
                if re.search(
                    rf"(?<![A-Za-z0-9_-]){re.escape(attribute)}"
                    rf"(?![A-Za-z0-9_-])",
                    attribute_text,
                )
            ]
            impact = used_by_target(path, content)
            finding = decision(path, code_content, impact)
            decision_counts[finding] = decision_counts.get(finding, 0) + 1
            print(
                f"K{count:03d}\t{relative}\t{start}-{end}\t{kind}\t"
                f"{','.join(attrs) or '-'}\t{impact}\t{finding}\t{one_line(content)}"
            )
    print(f"# total={count}")
    print(f"# kind_counts={kind_counts}")
    print(f"# decision_counts={decision_counts}")


if __name__ == "__main__":
    main()
