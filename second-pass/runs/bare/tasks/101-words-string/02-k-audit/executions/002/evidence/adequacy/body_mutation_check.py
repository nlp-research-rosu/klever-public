#!/usr/bin/env python3
"""Confirm that the body-sensitivity probe changes the executed claim term."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def digest(term: object) -> str:
    return hashlib.sha256(
        json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


submitted = json.loads(Path("/tmp/audit-work/solution-kast.json").read_text())["term"]
spec = json.loads(Path("/tmp/audit-work/body-sensitivity.json").read_text())
claim = spec["term"]["term"][0]["localSentences"][0]
mutation = claim["body"]["args"][0]["args"][0]["lhs"]["items"][0]

submitted_digest = digest(submitted)
mutation_digest = digest(mutation)
print(f"submitted_program_kast_sha256={submitted_digest}")
print(f"mutated_claim_program_kast_sha256={mutation_digest}")
print(f"executed_program_term_changed={submitted != mutation}")
assert submitted != mutation
print("BODY_MUTATION_CONSTRUCTOR_CHECK=PASS")
