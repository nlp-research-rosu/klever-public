#!/usr/bin/env bash
set -euo pipefail

sha256sum \
  /reference/lemma-discovery.json \
  /reference/k-proof/verification.k \
  /reference/klean-generation/generated/obligation-map.json \
  /reference/klean-generation/trust-inventory.json

PYTHONPATH=/reference python3 - <<'PY'
import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification
from tools.klean_export import tree_digest

def read(path):
    return json.loads(Path(path).read_text())

audit = read('/audit-input.json')
discovery = read('/reference/lemma-discovery.json')
input_manifest = read('/reference/klean-generation/input-manifest.json')
generator = read('/reference/klean-generation/generator-manifest.json')
export = read('/reference/klean-generation/export-result.json')
recorded_preflight = read('/reference/klean-generation/preflight.json')
obligation_map = read(
    '/reference/klean-generation/generated/obligation-map.json'
)
inventory = inventory_verification(Path('/reference/k-proof'))

# This set is supplied by the independent per-rule semantic judgment recorded
# in REVIEW.md and 05_classification_evidence.txt, not inferred from Stage 3.
independent_domain_ids = []
discovery_domain_ids = [
    rule['source_rule_id'] for rule in discovery['rules']
    if rule['classification'] == 'DOMAIN_LEMMA'
]
source_rule_ids = [
    rule['source_rule_id'] for rule in input_manifest['source_rules']
]
map_source_ids = [
    rule['source_rule_id'] for rule in obligation_map['source_rules']
]
obligation_ids = [
    obligation['source_rule_id']
    for obligation in obligation_map['obligations']
]

actual = {
    'discovery_manifest_sha256': hashlib.sha256(
        Path('/reference/lemma-discovery.json').read_bytes()
    ).hexdigest(),
    'verification_sha256': hashlib.sha256(
        Path('/reference/k-proof/verification.k').read_bytes()
    ).hexdigest(),
    'obligation_map_sha256': hashlib.sha256(
        Path('/reference/klean-generation/generated/obligation-map.json')
        .read_bytes()
    ).hexdigest(),
    'trust_inventory_sha256': hashlib.sha256(
        Path('/reference/klean-generation/trust-inventory.json').read_bytes()
    ).hexdigest(),
    'generated_tree_sha256': tree_digest(
        Path('/reference/klean-generation/generated')
    ),
    'stage1_workspace_sha256': tree_digest(Path('/reference/k-proof')),
}

checks = {
    'inventory_hash_input_manifest': (
        input_manifest['inventory_sha256'] == inventory['inventory_sha256']
    ),
    'inventory_hash_generator': (
        generator['provenance']['inventory_sha256']
        == inventory['inventory_sha256']
    ),
    'discovery_hash_input_manifest': (
        input_manifest['stage3_discovery_manifest_sha256']
        == actual['discovery_manifest_sha256']
    ),
    'discovery_hash_generator': (
        generator['provenance']['stage3_discovery_manifest_sha256']
        == actual['discovery_manifest_sha256']
    ),
    'discovery_hash_export': (
        export['stage3_discovery_manifest_sha256']
        == actual['discovery_manifest_sha256']
    ),
    'verification_hash_input_manifest': (
        input_manifest['verification_sha256'] == actual['verification_sha256']
    ),
    'stage1_hash_input_manifest': (
        input_manifest['stage1_workspace_sha256']
        == actual['stage1_workspace_sha256']
    ),
    'stage1_hash_generator': (
        generator['provenance']['stage1_workspace_sha256']
        == actual['stage1_workspace_sha256']
    ),
    'stage1_hash_export': (
        export['frozen_input_sha256'] == actual['stage1_workspace_sha256']
    ),
    'obligation_map_hash_generator': (
        generator['obligation_map_sha256']
        == actual['obligation_map_sha256']
    ),
    'trust_inventory_hash_export': (
        export['trust_inventory_sha256']
        == actual['trust_inventory_sha256']
    ),
    'generated_tree_hash_generator': (
        generator['generated_tree_sha256']
        == actual['generated_tree_sha256']
    ),
    'generated_tree_hash_export': (
        export['generated_tree_sha256']
        == actual['generated_tree_sha256']
    ),
    'generated_tree_hash_audit_input': (
        audit['resolution']['hashes']['generated_tree_sha256']
        == actual['generated_tree_sha256']
    ),
    'domain_set_matches_discovery': (
        independent_domain_ids == discovery_domain_ids
    ),
    'source_rule_bijection': (
        independent_domain_ids == source_rule_ids
        == map_source_ids == obligation_ids
    ),
    'unique_source_rule_ids': len(source_rule_ids) == len(set(source_rule_ids)),
    'unique_obligation_ids': len(obligation_ids) == len(set(obligation_ids)),
    'all_conjuncts_nonempty': all(
        isinstance(item.get('lean_conjunct'), str)
        and bool(item['lean_conjunct'])
        for item in obligation_map['obligations']
    ),
    'obligation_counts_all_zero': (
        generator['obligation_count']
        == export['obligation_count']
        == recorded_preflight['obligation_count']
        == len(obligation_map['obligations'])
        == 0
    ),
    'status_no_obligations': (
        export['status']
        == recorded_preflight['status']
        == audit['resolution']['selections']['klean_generation']['status']
        == 'KLEAN_NO_OBLIGATIONS'
    ),
    'all_targets_null': (
        generator['target'] is None
        and recorded_preflight['target'] is None
        and audit['resolution']['target'] is None
        and audit['resolution']['stage4_preflight']['target'] is None
    ),
    'classification_only_mode': (
        audit['resolution']['mode'] == 'CLASSIFICATION_ONLY'
    ),
    'no_stage5_binding': (
        audit['resolution']['lean_workspace'] is None
        and audit['resolution']['lean_invocation'] is None
        and audit['resolution']['stage5_result'] is None
    ),
    'candidate_absent': not Path('/candidate').exists(),
}

print(json.dumps({
    'actual_hashes': actual,
    'independent_domain_ids': independent_domain_ids,
    'discovery_domain_ids': discovery_domain_ids,
    'input_manifest_source_rule_ids': source_rule_ids,
    'obligation_map_source_rule_ids': map_source_ids,
    'obligation_ids': obligation_ids,
    'targets': {
        'generator_manifest': generator['target'],
        'recorded_preflight': recorded_preflight['target'],
        'audit_resolution': audit['resolution']['target'],
        'audit_stage4_preflight': (
            audit['resolution']['stage4_preflight']['target']
        ),
    },
    'checks': checks,
    'all_checks_pass': all(checks.values()),
}, indent=2, sort_keys=True))
PY

find /reference/klean-generation/generated \
  -maxdepth 3 -type f -printf '%P\n' | sort
sed -n '1,240p' \
  /reference/klean-generation/generated/Klean124ValidDate/Lemmas.lean
