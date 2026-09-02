#!/usr/bin/env python3
"""Check the bridge theorem is proved bridge-free before installation/use."""

from __future__ import annotations

import json
from pathlib import Path
import re


workspace = Path("/reference/k-proof")
claim_text = (workspace / "connection-spec.k").read_text(encoding="utf-8")
rule_text = (workspace / "connection-rule.k").read_text(encoding="utf-8")
prove_text = (workspace / "prove.sh").read_text(encoding="utf-8")
prove_log = (workspace / "prove.log").read_text(encoding="utf-8")

claim_match = re.search(
    r"(?ms)^\s*claim\s+\[search-loop\]:\s*(.*?)\s*^endmodule\s*$",
    claim_text,
)
rule_match = re.search(
    r"(?ms)^\s*rule\s*(.*?)\s*\[priority\(40\)\]\s*^endmodule\s*$",
    rule_text,
)
if claim_match is None or rule_match is None:
    raise SystemExit("could not extract bridge claim/rule")

normalize = lambda text: " ".join(text.split())
claim_statement = normalize(claim_match.group(1))
installed_statement = normalize(rule_match.group(1))

markers = {
    "compile_base": "kompile --backend haskell verification-base.k",
    "prove_connection": "kprove connection-spec.k",
    "compile_installed_rule": "kompile --backend haskell connection-rule.k",
    "compile_final": "kompile --backend haskell verification.k",
    "prove_final": "kprove spec.k",
}
positions = {name: prove_text.find(marker) for name, marker in markers.items()}
ordered = [
    positions["compile_base"],
    positions["prove_connection"],
    positions["compile_installed_rule"],
    positions["compile_final"],
    positions["prove_final"],
]

result = {
    "connection_spec_requires": re.findall(
        r'(?m)^\s*requires\s+"([^"]+)"', claim_text
    ),
    "connection_spec_imports_installed_rule": (
        "connection-rule.k" in re.findall(
            r'(?m)^\s*requires\s+"([^"]+)"', claim_text
        )
    ),
    "bridge_free_base_contains_installed_statement": (
        installed_statement
        in normalize((workspace / "verification-base.k").read_text(encoding="utf-8"))
    ),
    "claim_statement_normalized": claim_statement,
    "installed_rule_statement_normalized_without_priority": installed_statement,
    "exact_statement_match_ignoring_claim_label_and_operational_priority": (
        claim_statement == installed_statement
    ),
    "prove_script_marker_positions": positions,
    "proof_then_install_then_use_order": (
        all(position >= 0 for position in ordered)
        and ordered == sorted(ordered)
        and len(set(ordered)) == len(ordered)
    ),
    "prove_log_top_count": len(re.findall(r"(?m)^#Top$", prove_log)),
    "prove_log_unexpected_success_count": len(
        re.findall(r"UNEXPECTED SUCCESS", prove_log)
    ),
}
result["derived_lemma_criterion_met"] = (
    not result["connection_spec_imports_installed_rule"]
    and not result["bridge_free_base_contains_installed_statement"]
    and result[
        "exact_statement_match_ignoring_claim_label_and_operational_priority"
    ]
    and result["proof_then_install_then_use_order"]
    and result["prove_log_top_count"] >= 4
    and result["prove_log_unexpected_success_count"] == 0
)
print(json.dumps(result, indent=2, sort_keys=False))
