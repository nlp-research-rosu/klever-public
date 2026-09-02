#!/usr/bin/env python3
"""Static candidate/immutable-target integrity checks."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, "/reference")
from tools.klean_export import target_statement, tree_digest


candidate = Path("/candidate")
fresh = Path("/tmp/audit-work/33-sort-third-audit")
base = fresh / "Base"
reference_generated = Path("/reference/klean-generation/generated")
source_paths = sorted(
    path
    for path in candidate.rglob("*")
    if path.is_file()
    and not path.is_symlink()
    and ".lake" not in path.parts
    and path.suffix in {".lean", ".toml"}
)


def strip_lean_comments(text: str) -> str:
    output: list[str] = []
    index = 0
    block_depth = 0
    in_string = False
    while index < len(text):
        if block_depth:
            if text.startswith("/-", index):
                block_depth += 1
                index += 2
            elif text.startswith("-/", index):
                block_depth -= 1
                index += 2
            else:
                if text[index] == "\n":
                    output.append("\n")
                index += 1
            continue
        if in_string:
            output.append(text[index])
            if text[index] == "\\" and index + 1 < len(text):
                output.append(text[index + 1])
                index += 2
            else:
                if text[index] == '"':
                    in_string = False
                index += 1
            continue
        if text.startswith("/-", index):
            block_depth = 1
            index += 2
        elif text.startswith("--", index):
            newline = text.find("\n", index)
            if newline < 0:
                break
            output.append("\n")
            index = newline + 1
        else:
            output.append(text[index])
            if text[index] == '"':
                in_string = True
            index += 1
    return "".join(output)


source_text = "\n".join(path.read_text() for path in source_paths)
code_text = strip_lean_comments(source_text)
forbidden_patterns = {
    "sorry": r"\bsorry\b",
    "admit": r"\badmit\b",
    "unsafe": r"\bunsafe\b",
    "axiom_declaration": r"(?m)^\s*axiom\b",
    "opaque_declaration": r"(?m)^\s*opaque\b",
}
forbidden_hits = {
    name: re.findall(pattern, code_text)
    for name, pattern in forbidden_patterns.items()
}
parameter_names = [
    "«_<=Int_»",
    "«sortThirdResult(_)_VERIFICATION_ValSeq_ValSeq»",
    "«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»",
    "«vsLen(_)_MPY-CORE_Int_ValSeq»",
]
parameter_definition_counts = {
    name: len(
        re.findall(
            rf"(?m)^\s*def\s+{re.escape(name)}(?:\s|\(|:)",
            code_text,
        )
    )
    for name in parameter_names
}
candidate_target_declarations = len(
    re.findall(r"(?m)^\s*def\s+targetStatement\b", code_text)
)
candidate_final_declarations = len(
    re.findall(r"(?m)^\s*theorem\s+final\b", code_text)
)

checks = {
    "fresh_base_tree_matches_reference": (
        tree_digest(base) == tree_digest(reference_generated)
    ),
    "fresh_target_matches_reference_target": (
        target_statement(base) == target_statement(reference_generated)
    ),
    "candidate_does_not_shadow_target": candidate_target_declarations == 0,
    "candidate_has_one_final": candidate_final_declarations == 1,
    "candidate_has_each_parameter_definition_once": all(
        count == 1 for count in parameter_definition_counts.values()
    ),
    "candidate_has_no_forbidden_trust_tokens": not any(
        forbidden_hits.values()
    ),
}
print(
    json.dumps(
        {
            "candidate_source_paths": [
                path.relative_to(candidate).as_posix()
                for path in source_paths
            ],
            "fresh_base_tree_sha256": tree_digest(base),
            "reference_generated_tree_sha256": tree_digest(reference_generated),
            "candidate_target_declarations": candidate_target_declarations,
            "candidate_final_declarations": candidate_final_declarations,
            "parameter_definition_counts": parameter_definition_counts,
            "forbidden_hits": forbidden_hits,
            "checks": checks,
        },
        indent=2,
        sort_keys=True,
    )
)
if not all(checks.values()):
    raise SystemExit(1)
