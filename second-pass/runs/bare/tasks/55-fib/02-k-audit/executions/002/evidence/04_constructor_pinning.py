#!/usr/bin/env python3
"""Compare the freshly parsed program term with both submitted proof claims."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def label(term: dict) -> str | None:
    if term.get("node") != "KApply":
        return None
    return term["label"]["name"]


def child_by_label(term: dict, wanted: str) -> dict:
    for child in term.get("args", []):
        if isinstance(child, dict) and label(child) == wanted:
            return child
    raise AssertionError(f"missing child {wanted}")


def digest(term: dict) -> str:
    encoded = json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


scratch = Path("/tmp/audit-work/55-fib-independent-audit")
program_doc = json.loads((scratch / "program-kast.json").read_text())
spec_doc = json.loads((scratch / "fresh-spec-kast.json").read_text())
program = program_doc["term"]

modules = spec_doc["term"]["term"]
spec_module = next(module for module in modules if module["name"] == "SPEC")
claims = {
    sentence["att"]["att"]["label"]: sentence
    for sentence in spec_module["localSentences"]
    if sentence["node"] == "KClaim"
}
assert set(claims) == {"SPEC.fib-invoke", "SPEC.fib-module"}

module_config = claims["SPEC.fib-module"]["body"]["args"][0]
module_k_cell = child_by_label(module_config, "<k>")
module_rewrite = module_k_cell["args"][0]
assert module_rewrite["node"] == "KRewrite"
claimed_program = module_rewrite["lhs"]

program_stmts = program["args"][0]
program_func_def = program_stmts["args"][0]
program_body = program_func_def["args"][2]

invoke_config = claims["SPEC.fib-invoke"]["body"]["args"][0]
invoke_functions = child_by_label(invoke_config, "<functions>")["args"][0]
invoke_function = invoke_functions["args"][1]
invoke_body = invoke_function["args"][1]

module_functions = child_by_label(module_config, "<functions>")["args"][0]
assert module_functions["node"] == "KRewrite"
module_function = module_functions["rhs"]["args"][1]
module_registered_body = module_function["args"][1]

print(f"program_term_sha256={digest(program)}")
print(f"fib_module_lhs_sha256={digest(claimed_program)}")
print(f"program_body_sha256={digest(program_body)}")
print(f"fib_invoke_body_sha256={digest(invoke_body)}")
print(f"fib_module_registered_body_sha256={digest(module_registered_body)}")
print(f"module_lhs_equals_fresh_program={claimed_program == program}")
print(f"invoke_body_equals_fresh_program_body={invoke_body == program_body}")
print(f"module_registered_body_equals_fresh_program_body={module_registered_body == program_body}")

assert claimed_program == program
assert invoke_body == program_body
assert module_registered_body == program_body
