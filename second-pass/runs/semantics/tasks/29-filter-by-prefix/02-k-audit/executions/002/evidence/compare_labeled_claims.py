#!/usr/bin/env python3
"""Check that reviewer labels did not change either parsed claim."""

import json
from pathlib import Path


def claims(path: Path):
    document = json.loads(path.read_text())
    return document["term"]["term"][0]["localSentences"]


original = claims(Path("/audit-output/evidence/03-spec.json"))
labeled = claims(Path("/audit-output/evidence/03-spec-labeled.json"))
assert len(original) == len(labeled) == 2
results = [
    all(left[key] == right[key] for key in ("body", "requires", "ensures"))
    for left, right in zip(original, labeled)
]
print(f"CLAIM_BODY_REQUIRES_ENSURES_EQUAL={results}")
assert results == [True, True]
