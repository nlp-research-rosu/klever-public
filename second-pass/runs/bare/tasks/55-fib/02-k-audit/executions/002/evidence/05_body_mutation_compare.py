#!/usr/bin/env python3
"""Show that the negative body-sensitivity claim executes the mutated constructor term."""

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
    raise AssertionError(f"missing {wanted}")


def digest(term: dict) -> str:
    encoded = json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


scratch = Path("/tmp/audit-work/55-fib-independent-audit")
original = json.loads((scratch / "program-kast.json").read_text())["term"]
mutated = json.loads((scratch / "mutated-program-kast.json").read_text())["term"]
spec = json.loads((scratch / "body-mutation-spec-kast.json").read_text())
module = next(item for item in spec["term"]["term"] if item["name"] == "BODY-MUTATION-SPEC")
claim = next(item for item in module["localSentences"] if item["node"] == "KClaim")
config = claim["body"]["args"][0]
k_cell = child_by_label(config, "<k>")
claim_lhs = k_cell["args"][0]["lhs"]

print(f"original_program_sha256={digest(original)}")
print(f"mutated_program_sha256={digest(mutated)}")
print(f"body_mutation_claim_lhs_sha256={digest(claim_lhs)}")
print(f"original_differs_from_mutated={original != mutated}")
print(f"claim_executes_mutated_program={claim_lhs == mutated}")

assert original != mutated
assert claim_lhs == mutated
