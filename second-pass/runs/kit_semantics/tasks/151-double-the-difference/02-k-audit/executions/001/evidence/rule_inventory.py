#!/usr/bin/env python3
"""Exhaustive source-level K declaration/rule inventory for this audit."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys


ROOT = Path("/tmp/audit-work/candidate-src")
START = re.compile(
    r'^\s*(requires\s+"|module\b|endmodule\b|imports\b|configuration\b|'
    r"syntax\b|rule\b|claim\b|context\b)"
)


@dataclass
class Block:
    path: Path
    line: int
    kind: str
    text: str


def kind_of(line: str) -> str:
    stripped = line.strip()
    for kind in (
        "requires",
        "module",
        "endmodule",
        "imports",
        "configuration",
        "syntax",
        "rule",
        "claim",
        "context",
    ):
        if stripped.startswith(kind):
            return kind
    raise AssertionError(stripped)


def parse(path: Path) -> list[Block]:
    lines = path.read_text().splitlines()
    starts = [i for i, line in enumerate(lines) if START.match(line)]
    result: list[Block] = []
    for pos, start in enumerate(starts):
        end = starts[pos + 1] if pos + 1 < len(starts) else len(lines)
        block_lines = lines[start:end]
        while block_lines and (
            not block_lines[-1].strip() or block_lines[-1].lstrip().startswith("//")
        ):
            block_lines.pop()
        text = " ".join(
            part.strip()
            for line in block_lines
            if (part := line.strip()) and not part.startswith("//")
        )
        result.append(Block(path, start + 1, kind_of(lines[start]), text))
    return result


def flags(text: str) -> str:
    found: list[str] = []
    checks = [
        ("function", r"\bfunction\b"),
        ("total", r"\btotal\b"),
        ("functional", r"\bfunctional\b"),
        ("macro", r"\bmacro\b"),
        ("opaque/no-evaluators", r"\bno-evaluators\b"),
        ("symbol", r"\bsymbol\s*\("),
        ("priority", r"\bpriority\s*\("),
        ("simplification", r"\bsimplification(?:\s*\(|\b)"),
        ("concrete", r"\bconcrete\b"),
        ("symbolic", r"\bsymbolic\s*\("),
        ("owise", r"\bowise\b"),
        ("preserves-definedness", r"\bpreserves-definedness\b"),
        ("strict", r"\b(?:seq)?strict(?:\s*\(|\b)"),
    ]
    for label, pattern in checks:
        if re.search(pattern, text):
            found.append(label)
    return ",".join(found) if found else "-"


def relevance(path: Path, block: Block) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "verification.k":
        return "proof-local"
    if rel == "spec.k":
        return "entry-claim"
    if block.kind in ("requires", "module", "endmodule", "imports"):
        return "fixed-assembly"
    if rel == "reference-semantics/semantics.k":
        return "fixed-assembly"
    if rel == "reference-semantics/semantics/syntax.k":
        used_words = (
            "Int",
            "Float",
            "Bool",
            "Name",
            "BinOp",
            "Call",
            "Compare",
            "CmpOp",
            "Exprs",
            "Assign",
            "AugAssign",
            "For",
            "If",
            "Return",
            "Stmts",
            "Params",
            "ParamNames",
            "Module",
        )
        return "fixed-used-syntax" if any(word in block.text for word in used_words) else "fixed-unused"
    used_patterns = {
        "reference-semantics/semantics/core.k": (
            r"\b(configuration|ValSeq|Iterable|Val|Parent|Scope|KResult|"
            r"RetState|#loadAll|#look|builtinsScope|#evalArgs|#evalArgCont|"
            r"#applyK|Int\(|truthy\(B|applyBin|applyCmp|appendVal)\b"
        ),
        "reference-semantics/semantics/iter.k": r"#iterNext|#iterDone|#iterYield",
        "reference-semantics/semantics/list.k": r"#iterNext\(list",
        "reference-semantics/semantics/operators.k": (
            r"\b(BinOp|Compare|applyBin|applyCmp)\b"
        ),
        "reference-semantics/semantics/int.k": (
            r"applyBin\(\"(?:\+|%|\*)\"|pyMod|applyCmp\(\"(?:>|==)\""
        ),
        "reference-semantics/semantics/controls.k": (
            r"\b(Assign|AugAssign|If|#branch|For|#loop|#loopStep|"
            r"#bindTgt|#loopLbl)\b"
        ),
        "reference-semantics/semantics/functions.k": (
            r"\b(frame|#bindP|Return|#pop|#endcall)\b"
        ),
        "reference-semantics/semantics/builtins.k": (
            r"\b(applyBuiltin|isIntV)\b|\"isinstance\""
        ),
        "reference-semantics/semantics/call.k": (
            r"\b(Call|#callee|#evalArgs|#applyK|closureVal)\b"
        ),
        "reference-semantics/semantics/float.k": r"syntax Val\s*::=\s*Float",
    }
    pattern = used_patterns.get(rel)
    if pattern and re.search(pattern, block.text):
        return "fixed-used-slice"
    return "fixed-unreachable"


def main() -> int:
    files = [ROOT / "reference-semantics/semantics.k"]
    files.extend(sorted((ROOT / "reference-semantics/semantics").glob("*.k")))
    files.extend([ROOT / "verification.k", ROOT / "spec.k"])
    missing = [str(path) for path in files if not path.is_file()]
    if missing:
        print(f"ERROR missing={missing}")
        return 1

    totals: dict[str, int] = {}
    print("path\tline\tkind\tflags\trelevance\tdisposition\ttext")
    for path in files:
        for block in parse(path):
            totals[block.kind] = totals.get(block.kind, 0) + 1
            rel = path.relative_to(ROOT).as_posix()
            role = relevance(path, block)
            if role == "proof-local":
                disposition = "requires-individual-review"
            elif role == "entry-claim":
                disposition = "requires-adequacy-and-closure-review"
            elif role.startswith("fixed-used"):
                disposition = "trusted-supplied-baseline; inspect-executed-slice"
            elif role == "fixed-assembly":
                disposition = "trusted-supplied-baseline; assembly/declaration"
            else:
                disposition = "trusted-supplied-baseline; unreachable-by-program"
            print(
                f"{rel}\t{block.line}\t{block.kind}\t{flags(block.text)}\t"
                f"{role}\t{disposition}\t{block.text}"
            )
    print(f"TOTALS\t{totals}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
