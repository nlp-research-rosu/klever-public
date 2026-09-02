#!/usr/bin/env python3
"""Compare each installed Stage 3 rule to its earlier bridge-free K claim."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


workspace = Path("/reference/k-proof")
rules = inventory_verification(workspace)["rules"]
claim_source = (workspace / "loop-spec.k").read_text()
claim_labels = ("loop-empty", "loop-cons", "for-empty", "for-cons")


def normalized(text: str) -> str:
    return " ".join(text.split())


def claim_body(label: str) -> str:
    marker = re.search(rf"(?m)^\s*claim \[{re.escape(label)}\]:\s*$", claim_source)
    if marker is None:
        raise RuntimeError(f"missing claim {label}")
    following = re.search(r"(?m)^\s*(?:claim \[[^]]+\]:|endmodule)\s*$", claim_source[marker.end():])
    if following is None:
        raise RuntimeError(f"unterminated claim {label}")
    return claim_source[marker.end() : marker.end() + following.start()]


comparisons = []
for rule, label in zip(rules, claim_labels, strict=True):
    deployed = re.sub(r"^\s*rule\s+", "", rule["text"], count=1)
    deployed = re.sub(r"\s*\[priority\(40\)\]\s*$", "", deployed, count=1)
    proved = claim_body(label)
    deployed_normalized = normalized(deployed)
    proved_normalized = normalized(proved)
    comparisons.append(
        {
            "source_rule_id": rule["source_rule_id"],
            "claim": f"LOOP-SPEC.{label}",
            "same_transition_modulo_claim_label_and_deployment_priority": (
                deployed_normalized == proved_normalized
            ),
            "deployed_transition_sha256": hashlib.sha256(
                deployed_normalized.encode()
            ).hexdigest(),
            "proved_transition_sha256": hashlib.sha256(
                proved_normalized.encode()
            ).hexdigest(),
            "normalized_transition": deployed_normalized,
        }
    )

print(json.dumps(comparisons, indent=2, sort_keys=True))
if not all(
    item["same_transition_modulo_claim_label_and_deployment_priority"]
    for item in comparisons
):
    raise SystemExit(1)
