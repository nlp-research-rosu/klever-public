#!/usr/bin/env python3
"""Independently check that both proof macros denote the regenerated MPY AST."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


source = Path("/tmp/audit-work/11-string-xor-audit/source")
translated = (source / "solution.regenerated.mpy").read_text(encoding="utf-8")
verification = (source / "verification.k").read_text(encoding="utf-8")


def normalize(text: str) -> str:
    # MPY's omitted empty Stmts arguments parse as the explicit K list unit.
    return "".join(text.split()).replace(".Stmts", "")


program_region = verification.split("// BEGIN EXACT SOLUTION TERM", 1)[1]
program_region = program_region.split("// END EXACT SOLUTION TERM", 1)[0]
program_rhs = program_region.split("rule solutionProgram =>", 1)[1]

body_region = verification.split("rule solutionBody =>", 1)[1]
body_rhs = body_region.split("// Mathematical reference function", 1)[0]
body_as_module = (
    'Module(FuncDef("string_xor", Params("a", "b"),' + body_rhs + "))"
)

checks = {
    "solutionProgram_declaration_is_macro": bool(
        re.search(
            r'syntax\s+Module\s*::=\s*"solutionProgram"\s*\[macro\]',
            verification,
        )
    ),
    "solutionBody_declaration_is_macro": bool(
        re.search(
            r'syntax\s+Stmts\s*::=\s*"solutionBody"\s*\[macro\]',
            verification,
        )
    ),
    "one_solutionProgram_rule": len(
        re.findall(r"\brule\s+solutionProgram\s*=>", verification)
    )
    == 1,
    "one_solutionBody_rule": len(
        re.findall(r"\brule\s+solutionBody\s*=>", verification)
    )
    == 1,
    "solutionProgram_matches_regenerated_mpy": normalize(program_rhs)
    == normalize(translated),
    "solutionBody_matches_regenerated_function_body": normalize(body_as_module)
    == normalize(translated),
}

for name, result in checks.items():
    print(f"{name}: {result}")
print(
    "regenerated_mpy_sha256:",
    hashlib.sha256(translated.encode()).hexdigest(),
)
print(
    "solutionProgram_normalized_sha256:",
    hashlib.sha256(normalize(program_rhs).encode()).hexdigest(),
)
print(
    "solutionBody_wrapped_normalized_sha256:",
    hashlib.sha256(normalize(body_as_module).encode()).hexdigest(),
)

raise SystemExit(0 if all(checks.values()) else 1)
