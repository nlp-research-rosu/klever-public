#!/usr/bin/env python3
"""Compare a parsed submitted program with the LHS parsed from the claim."""

from __future__ import annotations

import json
import sys
from pathlib import Path


source_path = Path(sys.argv[1])
claim_rule_path = Path(sys.argv[2])
source = json.loads(source_path.read_text(encoding="utf-8"))
claim_rule = json.loads(claim_rule_path.read_text(encoding="utf-8"))

source_term = source["term"]
claim_rule_term = claim_rule["term"]
if claim_rule_term.get("node") != "KRewrite":
    raise RuntimeError("claim extraction did not parse as a rewrite")
claim_term = claim_rule_term["lhs"]

equal = source_term == claim_term
print(f"source_json={source_path}")
print(f"claim_rule_json={claim_rule_path}")
print(f"constructor_terms_equal={equal}")
if not equal:
    print(f"source_term={json.dumps(source_term, sort_keys=True)}")
    print(f"claim_term={json.dumps(claim_term, sort_keys=True)}")
    raise SystemExit(1)
