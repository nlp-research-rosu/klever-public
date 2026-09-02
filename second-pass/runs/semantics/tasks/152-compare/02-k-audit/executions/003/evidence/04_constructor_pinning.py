#!/usr/bin/env python3
"""Compare the expanded claim macro with the trusted translation's function term."""

from __future__ import annotations

import json
from pathlib import Path


def label(term: dict) -> str:
    return term.get("label", {}).get("name", "")


solution_document = json.loads(
    Path("/tmp/audit-work/152-compare/candidate/solution.kast.json").read_text(
        encoding="utf-8"
    )
)
macro_document = json.loads(
    Path("/tmp/audit-work/152-compare/candidate/compareDef.kast.json").read_text(
        encoding="utf-8"
    )
)

module_term = solution_document["term"]
assert label(module_term).startswith("Module("), label(module_term)
module_statements = module_term["args"][0]
assert label(module_statements).startswith("___MPY-SYNTAX_Stmts_"), label(
    module_statements
)
assert len(module_statements["args"]) == 2
translated_function = module_statements["args"][0]
empty_tail = module_statements["args"][1]
assert ".List{" in label(empty_tail) and label(empty_tail).endswith("_Stmts"), label(
    empty_tail
)

expanded_compare_def = macro_document["term"]
print(f"translated_function_label={label(translated_function)}")
print(f"expanded_compareDef_label={label(expanded_compare_def)}")
print(
    "constructor_terms_equal="
    f"{translated_function == expanded_compare_def}"
)
assert translated_function == expanded_compare_def

function_name = translated_function["args"][0]["token"]
print(f"function_name_token={function_name}")
print("module_has_exactly_one_function_statement=True")
print("pinning_check=PASS")
