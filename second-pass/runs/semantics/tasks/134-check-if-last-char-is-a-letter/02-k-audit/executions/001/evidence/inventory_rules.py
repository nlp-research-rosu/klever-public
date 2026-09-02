#!/usr/bin/env python3
"""Produce a line-located exhaustive declaration/rule inventory."""

from __future__ import annotations

import argparse
import hashlib
import re
from collections import Counter
from pathlib import Path


START = re.compile(
    r"^\s*(module|imports|configuration|syntax|context|rule|claim|alias|macro)\b"
)
ATTRS = (
    "function",
    "total",
    "functional",
    "simplification",
    "priority",
    "owise",
    "concrete",
    "symbol",
    "macro",
    "strict",
    "seqstrict",
)


def source_paths(root: Path) -> list[Path]:
    semantics_root = root / "reference-semantics"
    return (
        [semantics_root / "semantics.k"]
        + sorted((semantics_root / "semantics").glob("*.k"))
        + [root / "verification.k", root / "spec.k"]
    )


def declaration_blocks(path: Path) -> list[tuple[int, str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    blocks: list[tuple[int, str, str]] = []
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        first_match = START.match(lines[start])
        assert first_match is not None
        kind = first_match.group(1)
        body_lines = lines[start:end]
        while body_lines and (
            not body_lines[-1].strip()
            or body_lines[-1].lstrip().startswith("//")
            or body_lines[-1].strip() == "endmodule"
        ):
            body_lines.pop()
        blocks.append((start + 1, kind, "\n".join(body_lines)))
    return blocks


def detected_attributes(block: str) -> list[str]:
    code_only = "\n".join(line.split("//", 1)[0] for line in block.splitlines())
    bracket_contents = " ".join(re.findall(r"\[([^\]]+)\]", code_only))
    return [
        attr
        for attr in ATTRS
        if re.search(
            rf"(?<![A-Za-z0-9_-]){re.escape(attr)}(?![A-Za-z0-9_-])",
            bracket_contents,
        )
    ]


def function_symbol(block: str) -> str | None:
    if "function" not in detected_attributes(block):
        return None
    match = re.search(
        r"\bsyntax\s+\S+\s*::=\s*(?:\"([^\"]+)\"|([#A-Za-z][#A-Za-z0-9_-]*))",
        block,
        flags=re.S,
    )
    if match is None:
        return None
    return match.group(1) or match.group(2)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    paths = source_paths(args.root)
    all_blocks: dict[Path, list[tuple[int, str, str]]] = {}
    global_rules: list[str] = []
    for path in paths:
        blocks = declaration_blocks(path)
        all_blocks[path] = blocks
        global_rules.extend(body for _, kind, body in blocks if kind == "rule")

    function_declarations: list[tuple[Path, int, str, list[str]]] = []
    for path, blocks in all_blocks.items():
        for line, kind, block in blocks:
            if kind == "syntax":
                symbol = function_symbol(block)
                if symbol is not None:
                    function_declarations.append(
                        (path, line, symbol, detected_attributes(block))
                    )

    opaque_candidates: list[tuple[Path, int, str, list[str]]] = []
    for item in function_declarations:
        path, line, symbol, attrs = item
        rule_pattern = re.compile(
            rf"^\s*rule\s+{re.escape(symbol)}(?:\s|\()", flags=re.M
        )
        if not any(rule_pattern.search(rule) for rule in global_rules):
            opaque_candidates.append((path, line, symbol, attrs))

    out: list[str] = []
    out.append("EXHAUSTIVE K DECLARATION AND RULE INVENTORY")
    out.append(f"ROOT: {args.root}")
    out.append("")
    out.append("PER-FILE COUNTS")
    aggregate: Counter[str] = Counter()
    for path in paths:
        relative = path.relative_to(args.root)
        blocks = all_blocks[path]
        counts = Counter(kind for _, kind, _ in blocks)
        aggregate.update(counts)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        count_text = " ".join(f"{kind}={counts[kind]}" for kind in sorted(counts))
        out.append(f"{relative} sha256={digest} {count_text}")
    out.append(
        "AGGREGATE " + " ".join(f"{kind}={aggregate[kind]}" for kind in sorted(aggregate))
    )
    out.append("")
    out.append("FUNCTION / TOTAL / FUNCTIONAL DECLARATIONS")
    for path, line, symbol, attrs in function_declarations:
        relative = path.relative_to(args.root)
        out.append(
            f"{relative}:{line} symbol={symbol} attributes={','.join(attrs) or 'none'}"
        )
    out.append("")
    out.append("FUNCTIONS WITH NO LOCAL EQUATION (OPAQUE OR EXTERNALLY HOOKED CANDIDATES)")
    for path, line, symbol, attrs in opaque_candidates:
        relative = path.relative_to(args.root)
        out.append(
            f"{relative}:{line} symbol={symbol} attributes={','.join(attrs) or 'none'}"
        )
    if not opaque_candidates:
        out.append("(none)")
    out.append("")
    out.append("EVERY DECLARATION / RULE BLOCK")
    for path in paths:
        relative = path.relative_to(args.root)
        out.append("")
        out.append(f"===== {relative} =====")
        for line, kind, block in all_blocks[path]:
            attrs = detected_attributes(block)
            out.append(
                f"--- {relative}:{line} kind={kind} "
                f"attributes={','.join(attrs) or 'none'} ---"
            )
            out.append(block)

    args.output.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"output={args.output}")
    print(f"source_file_count={len(paths)}")
    print(
        "aggregate="
        + ",".join(f"{kind}:{aggregate[kind]}" for kind in sorted(aggregate))
    )
    print(f"function_declaration_count={len(function_declarations)}")
    print(f"opaque_candidate_count={len(opaque_candidates)}")
    print(f"inventory_lines={len(out)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
