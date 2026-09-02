#!/usr/bin/env python3
"""Compare the trusted-regenerated Module KAST with the claim's #loadAll argument."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument("solution_kast")
parser.add_argument("claim_rule_kast")
args = parser.parse_args()

solution_document = json.loads(Path(args.solution_kast).read_text(encoding="utf-8"))
claim_document = json.loads(Path(args.claim_rule_kast).read_text(encoding="utf-8"))
solution_term = solution_document["term"]
rewrite = claim_document["term"]
if rewrite.get("node") != "KRewrite":
    raise SystemExit("claim wrapper did not parse as KRewrite")
lhs = rewrite["lhs"]
if lhs.get("node") != "KApply" or not lhs["label"]["name"].startswith("#loadAll("):
    raise SystemExit("claim wrapper LHS is not #loadAll")
claim_module = lhs["args"][0]
rhs_module = rewrite["rhs"]["args"][0]

canonical_solution = json.dumps(solution_term, sort_keys=True, separators=(",", ":")).encode()
canonical_claim = json.dumps(claim_module, sort_keys=True, separators=(",", ":")).encode()
same = solution_term == claim_module
same_rhs = claim_module == rhs_module

print(f"solution_module_sha256={hashlib.sha256(canonical_solution).hexdigest()}")
print(f"claim_module_sha256={hashlib.sha256(canonical_claim).hexdigest()}")
print(f"constructor_level_equal={str(same).lower()}")
print(f"wrapper_lhs_rhs_equal={str(same_rhs).lower()}")
if not same or not same_rhs:
    raise SystemExit(1)
print("PROGRAM_PINNING_OK")
