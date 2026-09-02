#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract
from tools.klean_audit_contract import verify_stage6_audit_input


audit_path = Path("/audit-input.json")
audit = json.loads(audit_path.read_text())
resolution = audit["resolution"]
expected = resolution["hashes"]


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


observed = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-proof")
    ),
    "stage1_export_sha256": klean_export.tree_digest(
        Path("/reference/k-proof")
    ),
    "discovery_manifest_sha256": file_sha256(
        Path("/reference/lemma-discovery.json")
    ),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "generated_tree_sha256": klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/candidate")
    ),
}

source_expected = resolution["stage1_source_hashes"]
source_observed = {
    relative: file_sha256(Path("/reference/k-proof") / relative)
    for relative in source_expected
}

verified_resolution, verified_digest = verify_stage6_audit_input(audit)
print(
    json.dumps(
        {
            "audit_input_contract": {
                "verified_digest": verified_digest,
                "recorded_digest": audit["resolved_input_sha256"],
                "match": verified_digest == audit["resolved_input_sha256"],
                "verified_mode": verified_resolution["mode"],
            },
            "mounted_hashes": {
                key: {
                    "expected": expected[key],
                    "observed": value,
                    "match": expected[key] == value,
                }
                for key, value in observed.items()
            },
            "stage1_source_hashes": {
                relative: {
                    "expected": source_expected[relative],
                    "observed": source_observed[relative],
                    "match": source_expected[relative]
                    == source_observed[relative],
                }
                for relative in source_expected
            },
            "unmounted_recorded_hashes_not_used_as_evidence": {
                "lean_invocation_sha256": expected["lean_invocation_sha256"],
            },
        },
        indent=2,
        sort_keys=True,
    )
)
