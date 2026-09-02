#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path

from tools.k_rule_inventory import inventory_verification
from tools.klean_export import (
    expected_target_definition,
    target_statement,
    tree_digest,
)
from tools.pipeline_contract import sha256_tree

stage1 = Path('/reference/k-proof')
discovery_path = Path('/reference/lemma-discovery.json')
generation = Path('/reference/klean-generation')
generated = generation / 'generated'
audit = json.loads(Path('/audit-input.json').read_text())['resolution']
discovery = json.loads(discovery_path.read_text())
inventory = inventory_verification(stage1)
input_manifest = json.loads((generation / 'input-manifest.json').read_text())
generator = json.loads((generation / 'generator-manifest.json').read_text())
export_result = json.loads((generation / 'export-result.json').read_text())
obligation_path = generated / 'obligation-map.json'
obligation_map = json.loads(obligation_path.read_text())

manifest_by_id = {r['source_rule_id']: r for r in discovery['rules']}
independent_domain_ids = []  # Established by the rule-by-rule semantic audit.
protected_domain_ids = [r['source_rule_id'] for r in discovery['rules'] if r['classification'] == 'DOMAIN_LEMMA']
input_domain_ids = [r['source_rule_id'] for r in input_manifest['source_rules']]
mapped_source_ids = [r['source_rule_id'] for r in obligation_map['source_rules']]
obligation_ids = [r['source_rule_id'] for r in obligation_map['obligations']]
definition_ids = [r['source_rule_id'] for r in input_manifest['definitions']]
inventory_ids = [r['source_rule_id'] for r in inventory['rules']]
expected_definitions = []
for rule in inventory['rules']:
    classified = manifest_by_id[rule['source_rule_id']]
    if classified['classification'] == 'DEFINITION':
        expected_definitions.append({**rule, **classified})

lean_files = sorted(generated.rglob('*.lean'))
target_declaration_matches = []
for path in lean_files:
    for match in re.finditer(r'(?m)^\s*def\s+targetStatement\b', path.read_text()):
        target_declaration_matches.append(f'{path.relative_to(generated)}:{path.read_text()[:match.start()].count(chr(10)) + 1}')

checks = {
    'audit_stage1_pipeline_tree_hash': sha256_tree(stage1) == audit['hashes']['k_workspace_sha256'],
    'audit_stage1_export_tree_hash': tree_digest(stage1) == audit['hashes']['stage1_export_sha256'],
    'audit_discovery_file_hash': hashlib.sha256(discovery_path.read_bytes()).hexdigest() == audit['hashes']['discovery_manifest_sha256'],
    'audit_generation_pipeline_tree_hash': sha256_tree(generation) == audit['hashes']['klean_generation_sha256'],
    'audit_generated_export_tree_hash': tree_digest(generated) == audit['hashes']['generated_tree_sha256'],
    'generator_generated_tree_hash': tree_digest(generated) == generator['generated_tree_sha256'],
    'generator_obligation_map_hash': hashlib.sha256(obligation_path.read_bytes()).hexdigest() == generator['obligation_map_sha256'],
    'input_inventory_hash': input_manifest['inventory_sha256'] == inventory['inventory_sha256'],
    'generator_inventory_hash': generator['provenance']['inventory_sha256'] == inventory['inventory_sha256'],
    'input_verification_hash': input_manifest['verification_sha256'] == inventory['verification_sha256'],
    'input_definitions_exact_order': definition_ids == inventory_ids,
    'input_definition_records_exact': input_manifest['definitions'] == expected_definitions,
    'input_definitions_unique': len(definition_ids) == len(set(definition_ids)),
    'independent_domain_set_empty': independent_domain_ids == [],
    'protected_domain_set_matches_independent': protected_domain_ids == independent_domain_ids,
    'input_domain_set_matches_independent': input_domain_ids == independent_domain_ids,
    'mapped_source_set_matches_independent': mapped_source_ids == independent_domain_ids,
    'obligation_set_matches_independent': obligation_ids == independent_domain_ids,
    'obligation_ids_unique': len(obligation_ids) == len(set(obligation_ids)),
    'no_trust_parameters': obligation_map['trust_parameters'] == [],
    'obligation_count_zero': generator['obligation_count'] == export_result['obligation_count'] == 0,
    'export_status_no_obligations': export_result['status'] == 'KLEAN_NO_OBLIGATIONS',
    'expected_target_definition_absent': expected_target_definition(obligation_map) is None,
    'trusted_target_parser_absent': target_statement(generated) is None,
    'no_lean_target_declaration': target_declaration_matches == [],
    'generator_target_null': generator['target'] is None,
    'audit_target_null': audit.get('target') is None,
    'selected_status_no_obligations': audit['selections']['klean_generation']['status'] == 'KLEAN_NO_OBLIGATIONS',
}
print('COMMAND: independently verify all Stage 4 hashes, exact rule/obligation bijection, and fixed null target')
for key, value in checks.items():
    print(f'{key}: {value}')
print(f'inventory_ids={inventory_ids!r}')
print(f'independent_domain_ids={independent_domain_ids!r}')
print(f'protected_domain_ids={protected_domain_ids!r}')
print(f'input_domain_ids={input_domain_ids!r}')
print(f'mapped_source_ids={mapped_source_ids!r}')
print(f'obligation_ids={obligation_ids!r}')
print(f'target_declaration_matches={target_declaration_matches!r}')
if not all(checks.values()):
    raise SystemExit('STAGE4_INDEPENDENT_GATE_FAILED')
print('STAGE4_INDEPENDENT_GATE: PASS')
