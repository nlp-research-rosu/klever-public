#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract


audit_input = json.loads(Path("/audit-input.json").read_text())
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
    audit_input
)
expected_hashes = resolution["hashes"]

observed_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-proof")
    ),
    "stage1_export_sha256": klean_export.tree_digest(
        Path("/reference/k-proof")
    ),
    "discovery_manifest_sha256": pipeline_contract.sha256_file(
        Path("/reference/lemma-discovery.json")
    ),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generated_tree_sha256": klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/candidate")
    ),
}

stage1_source_checks = {}
for relative, expected in resolution["stage1_source_hashes"].items():
    actual = hashlib.sha256(
        (Path("/reference/k-proof") / relative).read_bytes()
    ).hexdigest()
    stage1_source_checks[relative] = {
        "expected": expected,
        "actual": actual,
        "matches": actual == expected,
    }

generation = Path("/reference/klean-generation")
generated = generation / "generated"
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
export_result = json.loads((generation / "export-result.json").read_text())
target_from_source = klean_export.target_statement(generated)
expected_target_definition = klean_export.expected_target_definition(
    json.loads((generated / "obligation-map.json").read_text())
)
actual_definition_matches_expected = (
    target_from_source["definition_sha256"]
    == klean_export.sha256_text(expected_target_definition)
)

manifest_hash_checks = {
    "exporter_sha256": {
        "expected": generator_manifest["exporter_sha256"],
        "actual": hashlib.sha256(
            Path("/reference/tools/klean_export.py").read_bytes()
        ).hexdigest(),
    },
    "klean_py_sha256": {
        "expected": generator_manifest["klean_py_sha256"],
        "actual": hashlib.sha256(
            Path("/reference/tools/klean.py").read_bytes()
        ).hexdigest(),
    },
    "obligation_map_sha256": {
        "expected": generator_manifest["obligation_map_sha256"],
        "actual": hashlib.sha256(
            (generated / "obligation-map.json").read_bytes()
        ).hexdigest(),
    },
    "trust_inventory_sha256": {
        "expected": export_result["trust_inventory_sha256"],
        "actual": hashlib.sha256(
            (generation / "trust-inventory.json").read_bytes()
        ).hexdigest(),
    },
}
for check in manifest_hash_checks.values():
    check["matches"] = check["actual"] == check["expected"]

candidate_text = Path("/candidate/Proof.lean").read_text()
forbidden_matches = re.findall(
    r"\b(?:sorry|admit|unsafe|axiom|opaque)\b", candidate_text
)
target_count_candidate = len(
    re.findall(r"(?m)^\s*def\s+targetStatement\b", candidate_text)
)
final_statements = re.findall(
    r"(?ms)^\s*theorem\s+final\s*:\s*(.*?)\s*:=\s*by\b",
    candidate_text,
)
normalized_final_statement = (
    " ".join(final_statements[0].split()) if len(final_statements) == 1 else None
)

hash_matches = {
    key: observed == expected_hashes[key]
    for key, observed in observed_hashes.items()
}
target_checks = {
    "generator_manifest_equals_source": (
        generator_manifest["target"] == target_from_source
    ),
    "audit_input_equals_source": resolution["target"] == target_from_source,
    "stage4_preflight_equals_source": (
        resolution["stage4_preflight"]["target"] == target_from_source
    ),
    "definition_is_exact_obligation_conjunction": (
        actual_definition_matches_expected
    ),
    "candidate_does_not_redeclare_target": target_count_candidate == 0,
    "candidate_final_statement_exact": (
        normalized_final_statement
        == " ".join(target_from_source["statement"].split())
    ),
    "candidate_has_no_forbidden_tokens": not forbidden_matches,
}

result = {
    "resolved_input_sha256": {
        "expected": audit_input["resolved_input_sha256"],
        "actual": resolved_digest,
        "matches": resolved_digest == audit_input["resolved_input_sha256"],
    },
    "mounted_hashes": {
        key: {
            "expected": expected_hashes[key],
            "actual": observed_hashes[key],
            "matches": hash_matches[key],
        }
        for key in observed_hashes
    },
    "unmounted_hashes": {
        "lean_invocation_sha256": {
            "expected": expected_hashes["lean_invocation_sha256"],
            "status": "not independently recomputable: launcher did not mount the Stage 5 invocation tree",
        }
    },
    "stage1_source_hashes": stage1_source_checks,
    "manifest_hashes": manifest_hash_checks,
    "target_from_source": target_from_source,
    "target_checks": target_checks,
    "candidate_forbidden_matches": forbidden_matches,
    "all_mounted_checks_pass": (
        resolved_digest == audit_input["resolved_input_sha256"]
        and all(hash_matches.values())
        and all(item["matches"] for item in stage1_source_checks.values())
        and all(item["matches"] for item in manifest_hash_checks.values())
        and all(target_checks.values())
    ),
}
print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
