#!/usr/bin/env python3
"""Mechanical token-level comparison of translated and claimed function bodies."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/rebuild")


def compact(text: str) -> str:
    text = re.sub(r"//.*", "", text)
    return re.sub(r"\s+", "", text)


def normalize_list_syntax(text: str) -> str:
    # py2mpy omits empty K list terminators where K's list parser permits that;
    # the candidate macros spell those same terminators explicitly.
    return compact(text).replace(".Stmts", "").replace(".Exprs", "")


solution = compact((ROOT / "solution.regenerated.mpy").read_text())
prefix = 'Module(FuncDef("odd_count",Params("lst"),'
assert solution.startswith(prefix), solution[:120]
assert solution.endswith("))"), solution[-120:]
translated_body = solution[len(prefix) : -2]

verification = (ROOT / "verification.k").read_text()
outer_match = re.search(
    r"rule\s+ODD-COUNT-BODY\s*=>\s*(.*?)"
    r"(?=\n\s*rule\s+ODD-COUNT-LOOP-BODY)",
    verification,
    re.DOTALL,
)
loop_match = re.search(
    r"rule\s+ODD-COUNT-LOOP-BODY\s*=>\s*(.*?)"
    r"(?=\n\s*rule\s+isStringVal)",
    verification,
    re.DOTALL,
)
assert outer_match is not None
assert loop_match is not None

loop_body = normalize_list_syntax(loop_match.group(1))
claimed_body = normalize_list_syntax(outer_match.group(1))
claimed_body = claimed_body.replace("ODD-COUNT-LOOP-BODY", loop_body)
translated_body = normalize_list_syntax(translated_body)

translated_hash = hashlib.sha256(translated_body.encode()).hexdigest()
claimed_hash = hashlib.sha256(claimed_body.encode()).hexdigest()
print(f"translated_body_sha256={translated_hash}")
print(f"claimed_expanded_body_sha256={claimed_hash}")
print(f"constructor_body_exact_match={translated_body == claimed_body}")

if translated_body != claimed_body:
    mismatch = next(
        (
            index
            for index, (left, right) in enumerate(
                zip(translated_body, claimed_body, strict=False)
            )
            if left != right
        ),
        min(len(translated_body), len(claimed_body)),
    )
    print(f"first_mismatch_offset={mismatch}")
    print(f"translated_context={translated_body[mismatch:mismatch + 160]}")
    print(f"claimed_context={claimed_body[mismatch:mismatch + 160]}")
    raise SystemExit(1)
