#!/usr/bin/env python3
"""Compare the translated function body with the expanded proof macro."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def compact(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


solution = json.loads(
    Path("/tmp/audit-work/recon/solution.kast.json").read_text()
)["term"]
macro_body = json.loads(
    Path("/tmp/audit-work/recon/body.kast.json").read_text()
)["term"]

assert solution["label"]["name"] == "Module(_)_MPY-SYNTAX_Module_Stmts"
statements = solution["args"][0]
assert statements["label"]["name"].startswith("___MPY-SYNTAX_Stmts_")
function = statements["args"][0]
tail = statements["args"][1]

name_token, params, translated_body = function["args"]
name = name_token["token"]
param_name = params["args"][0]["args"][0]["token"]
tail_label = tail["label"]["name"]

body_equal = translated_body == macro_body
translated_digest = hashlib.sha256(compact(translated_body)).hexdigest()
macro_digest = hashlib.sha256(compact(macro_body)).hexdigest()

print(f"translated_function_name={name}")
print(f"translated_parameter={param_name}")
print(f"translated_module_tail_label={tail_label}")
print(f"translated_body_sha256={translated_digest}")
print(f"expanded_strangeBody_sha256={macro_digest}")
print(f"body_json_equal={body_equal}")

if name != '"strange_sort_list"' or param_name != '"lst"':
    raise SystemExit("unexpected translated entry point")
if not tail_label.startswith(".List"):
    raise SystemExit("solution.mpy contains unexpected top-level statements")
raise SystemExit(0 if body_equal else 1)
