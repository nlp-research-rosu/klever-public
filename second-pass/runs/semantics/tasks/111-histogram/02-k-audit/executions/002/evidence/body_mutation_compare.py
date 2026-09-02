#!/usr/bin/env python3
"""Require the body mutation to alter the function term executed by the claim."""

import hashlib
import json
from pathlib import Path


WORK = Path("/tmp/audit-work/111-histogram")


def function_term(path: Path) -> object:
    term = json.loads(path.read_text())["term"]
    return term["args"][0]["args"][0]


def digest(term: object) -> str:
    return hashlib.sha256(
        json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


original = function_term(WORK / "wrapper-kast.json")
mutated = function_term(WORK / "body-mutation-wrapper-kast.json")
print(f"ORIGINAL_FUNCTION_CONSTRUCTOR_SHA256={digest(original)}")
print(f"MUTATED_FUNCTION_CONSTRUCTOR_SHA256={digest(mutated)}")
print(f"MUTATION_CHANGED_EXECUTED_FUNCTION_TERM={original != mutated}")
if original == mutated:
    raise SystemExit(1)
