#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import pipeline_contract
from tools.klean_export import tree_digest
from tools.stage6_resolution_contract import canonical_json_sha256, verify_audit_input

audit_path = Path('/audit-input.json')
document = json.loads(audit_path.read_text())
resolution, signed_digest = verify_audit_input(document)
stage1 = Path('/reference/k-proof')
k_audit = Path('/reference/k-audit')
discovery = Path('/reference/lemma-discovery.json')
generation = Path('/reference/klean-generation')
generated = generation / 'generated'
producer = Path('/reference/generation-tools')
input_manifest = json.loads((generation / 'input-manifest.json').read_text())
generator = json.loads((generation / 'generator-manifest.json').read_text())
export_result = json.loads((generation / 'export-result.json').read_text())
trust_inventory = generation / 'trust-inventory.json'

expected_source_hashes = resolution['stage1_source_hashes']
observed_source_hashes = {
    path.relative_to(stage1).as_posix(): pipeline_contract.sha256_file(path)
    for path in pipeline_contract._walk_regular_files(stage1, 'Stage 1 source workspace')
}
missing_source_paths = sorted(set(expected_source_hashes) - set(observed_source_hashes))
extra_source_paths = sorted(set(observed_source_hashes) - set(expected_source_hashes))
mismatched_source_paths = sorted(
    path for path in set(expected_source_hashes) & set(observed_source_hashes)
    if expected_source_hashes[path] != observed_source_hashes[path]
)

hashes = resolution['hashes']
checks = {
    'signed_envelope_verified': canonical_json_sha256(resolution) == signed_digest == document['resolved_input_sha256'],
    'stage1_pipeline_tree': pipeline_contract.sha256_tree(stage1) == hashes['k_workspace_sha256'],
    'stage1_export_tree': tree_digest(stage1) == hashes['stage1_export_sha256'],
    'stage1_source_file_set_and_hashes': not missing_source_paths and not extra_source_paths and not mismatched_source_paths,
    'selected_stage2_tree': pipeline_contract.sha256_tree(k_audit) == hashes['k_audit_sha256'],
    'stage3_file': pipeline_contract.sha256_file(discovery) == hashes['discovery_manifest_sha256'],
    'stage4_pipeline_tree': pipeline_contract.sha256_tree(generation) == hashes['klean_generation_sha256'],
    'generated_export_tree': tree_digest(generated) == hashes['generated_tree_sha256'],
    'producer_pipeline_tree': pipeline_contract.sha256_tree(producer) == hashes['generation_producer_sources_sha256'],
    'classification_only_lean_hashes_null': hashes['lean_invocation_sha256'] is None and hashes['lean_workspace_sha256'] is None,
    'classification_only_lean_paths_null': resolution['lean_invocation'] is None and resolution['lean_workspace'] is None,
    'classification_only_stage5_result_null': resolution['stage5_result'] is None,
    'selected_stage2_artifact_hash': resolution['selections']['k_audit']['artifact_sha256'] == hashes['k_audit_sha256'],
    'selected_stage4_artifact_hash': resolution['selections']['klean_generation']['artifact_sha256'] == hashes['klean_generation_sha256'],
    'input_frozen_hash': input_manifest['frozen_input_sha256'] == tree_digest(stage1),
    'input_stage1_hash': input_manifest['stage1_workspace_sha256'] == tree_digest(stage1),
    'input_stage3_hash': input_manifest['stage3_discovery_manifest_sha256'] == pipeline_contract.sha256_file(discovery),
    'input_verification_hash': input_manifest['verification_sha256'] == hashlib.sha256((stage1 / 'verification.k').read_bytes()).hexdigest(),
    'generator_stage1_provenance': generator['provenance']['stage1_workspace_sha256'] == tree_digest(stage1),
    'generator_stage3_provenance': generator['provenance']['stage3_discovery_manifest_sha256'] == pipeline_contract.sha256_file(discovery),
    'generator_generated_hash': generator['generated_tree_sha256'] == tree_digest(generated),
    'generator_obligation_map_hash': generator['obligation_map_sha256'] == hashlib.sha256((generated / 'obligation-map.json').read_bytes()).hexdigest(),
    'export_frozen_hash': export_result['frozen_input_sha256'] == tree_digest(stage1),
    'export_stage3_hash': export_result['stage3_discovery_manifest_sha256'] == pipeline_contract.sha256_file(discovery),
    'export_generated_hash': export_result['generated_tree_sha256'] == tree_digest(generated),
    'export_trust_inventory_hash': export_result['trust_inventory_sha256'] == hashlib.sha256(trust_inventory.read_bytes()).hexdigest(),
    'launcher_preflight_stage1_hash': resolution['stage4_preflight']['stage1_workspace_sha256'] == tree_digest(stage1),
    'launcher_preflight_stage3_hash': resolution['stage4_preflight']['stage3_discovery_manifest_sha256'] == pipeline_contract.sha256_file(discovery),
    'launcher_preflight_generated_hash': resolution['stage4_preflight']['generated_tree_sha256'] == tree_digest(generated),
    'launcher_target_null': resolution['target'] is None,
}

print('COMMAND: verify signed launcher envelope, every launcher tree/file hash, every Stage 1 source-file hash, and manifest hash bindings')
for key, value in checks.items():
    print(f'{key}: {value}')
print(f'signed_resolution_sha256={signed_digest}')
print(f'stage1_expected_source_file_count={len(expected_source_hashes)}')
print(f'stage1_observed_source_file_count={len(observed_source_hashes)}')
print(f'missing_source_paths={missing_source_paths!r}')
print(f'extra_source_paths={extra_source_paths!r}')
print(f'mismatched_source_paths={mismatched_source_paths!r}')
if not all(checks.values()):
    raise SystemExit('LAUNCHER_OR_MANIFEST_INTEGRITY_FAILED')
print('LAUNCHER_AND_MANIFEST_INTEGRITY: PASS')
