#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import k_rule_inventory, stage6_resolution_contract


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_input = json.loads(Path("/audit-input.json").read_text())
resolution = audit_input["resolution"]
workspace = Path("/reference/k-proof")
inventory = k_rule_inventory.inventory_verification(workspace)
stage1_expected = resolution["stage1_source_hashes"]
stage1_observed = {
    path.relative_to(workspace).as_posix(): sha256(path)
    for path in sorted(workspace.rglob("*"))
    if path.is_file() and not path.is_symlink()
}

toolchain_lock = json.loads(Path("/reference/klean-toolchain.lock.json").read_text())
generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)

loop_rule = next(
    rule
    for rule in inventory["rules"]
    if rule["source_rule_id"]
    == "rule-7a0b234f2c7d2f2e9f5ca663b20c6f7b0d9cfa7eb71ea38b3a1681cb48235035"
)
rule_body = re.sub(r"^\s*rule\s*", "", loop_rule["text"], count=1)
rule_body = re.sub(
    r"\s*\[priority\(40\),\s*label\(factorize-loop-lemma\)\]\s*$",
    "",
    rule_body,
)

spec_text = (workspace / "spec.k").read_text()
claim_match = re.search(
    r"claim\s+\[factorize-loop\]:\s*(.*?)\n\s*endmodule",
    spec_text,
    flags=re.S,
)
if claim_match is None:
    raise RuntimeError("factorize-loop claim not found")
claim_body = claim_match.group(1)
normalize = lambda value: " ".join(value.split())

prove_script = (workspace / "prove.sh").read_text()
command_markers = [
    "--main-module FACTORIZE-VERIFICATION",
    "--spec-module FACTORIZE-LOOP-SPEC",
    "--main-module FACTORIZE-VERIFICATION-WITH-LOOP-LEMMA",
    "--spec-module FACTORIZE-SPEC",
]
marker_offsets = [prove_script.find(marker) for marker in command_markers]

result = {
    "audit_input_envelope": {
        "recorded_resolved_input_sha256": audit_input["resolved_input_sha256"],
        "recomputed_resolved_input_sha256": (
            stage6_resolution_contract.canonical_json_sha256(resolution)
        ),
        "matches": audit_input["resolved_input_sha256"]
        == stage6_resolution_contract.canonical_json_sha256(resolution),
    },
    "stage1_source_hashes": {
        "expected_count": len(stage1_expected),
        "observed_count": len(stage1_observed),
        "missing": sorted(set(stage1_expected) - set(stage1_observed)),
        "extra": sorted(set(stage1_observed) - set(stage1_expected)),
        "mismatches": {
            name: {
                "expected": stage1_expected[name],
                "observed": stage1_observed.get(name),
            }
            for name in stage1_expected
            if stage1_observed.get(name) != stage1_expected[name]
        },
        "all_match": stage1_expected == stage1_observed,
        "observed": stage1_observed,
    },
    "toolchain_lock": {
        "file_sha256": sha256(Path("/reference/klean-toolchain.lock.json")),
        "file_document": toolchain_lock,
        "generator_manifest_document": generator_manifest["toolchain"],
        "documents_equal": toolchain_lock == generator_manifest["toolchain"],
    },
    "proved_derived_lemma_identity": {
        "rule_source_rule_id": loop_rule["source_rule_id"],
        "rule_span": [loop_rule["start_line"], loop_rule["end_line"]],
        "normalized_rule_body": normalize(rule_body),
        "normalized_claim_body": normalize(claim_body),
        "exact_body_after_keyword_and_attribute_erasure": normalize(rule_body)
        == normalize(claim_body),
        "base_verification_module_imports_with_lemma": bool(
            re.search(
                r"module\s+FACTORIZE-VERIFICATION\b.*?"
                r"imports\s+FACTORIZE-VERIFICATION-WITH-LOOP-LEMMA",
                (workspace / "verification.k").read_text(),
                flags=re.S,
            )
        ),
        "loop_spec_imports_base_module": bool(
            re.search(
                r"module\s+FACTORIZE-LOOP-SPEC\b.*?"
                r"imports\s+FACTORIZE-VERIFICATION\b",
                spec_text,
                flags=re.S,
            )
        ),
        "command_markers": command_markers,
        "command_marker_offsets": marker_offsets,
        "command_markers_all_present_and_ordered": (
            all(offset >= 0 for offset in marker_offsets)
            and marker_offsets == sorted(marker_offsets)
        ),
    },
}

print(json.dumps(result, indent=2, sort_keys=True))
