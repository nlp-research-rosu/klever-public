#!/usr/bin/env python3
"""Compare the normalized K constructor trees for solution.mpy and entry claim."""

from __future__ import annotations

import hashlib
import json
import pathlib
from collections import Counter


SCRATCH = pathlib.Path("/tmp/audit-work/33-sort-third")
translated = json.loads((SCRATCH / "translated-program.json").read_text())["term"]
claimed_rewrite = json.loads((SCRATCH / "claimed-rule.json").read_text())["term"]
assert claimed_rewrite["node"] == "KRewrite"
claimed = claimed_rewrite["lhs"]


def canonical_hash(term: object) -> str:
    encoded = json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def inventory(term: object, counts: Counter[str]) -> None:
    if isinstance(term, dict):
        if term.get("node") == "KApply":
            counts[term["label"]["name"]] += 1
        for value in term.values():
            inventory(value, counts)
    elif isinstance(term, list):
        for value in term:
            inventory(value, counts)


translated_counts: Counter[str] = Counter()
claimed_counts: Counter[str] = Counter()
inventory(translated, translated_counts)
inventory(claimed, claimed_counts)
print(f"translated_sha256={canonical_hash(translated)}")
print(f"claimed_sha256={canonical_hash(claimed)}")
print(f"constructor_tree_exact_equal={translated == claimed}")
print(f"translated_kapply_nodes={sum(translated_counts.values())}")
print(f"claimed_kapply_nodes={sum(claimed_counts.values())}")
print(f"constructor_label_inventory_equal={translated_counts == claimed_counts}")
if translated != claimed:
    raise SystemExit(1)
