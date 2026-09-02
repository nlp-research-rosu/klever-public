#!/usr/bin/env python3
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.path.insert(0, '/reference/generation-tools')
spec = importlib.util.spec_from_file_location(
    'generation_klean_export',
    '/reference/generation-tools/klean_export.py',
)
producer = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = producer
spec.loader.exec_module(producer)

from tools.k_rule_inventory import inventory_verification

stage1 = Path('/reference/k-proof')
discovery_path = Path('/reference/lemma-discovery.json')
generation = Path('/reference/klean-generation')
generated = generation / 'generated'

inventory = inventory_verification(stage1)
discovery_bytes = discovery_path.read_bytes()
discovery = json.loads(discovery_bytes)
obligation_bytes = (generated / 'obligation-map.json').read_bytes()
obligation_map = json.loads(obligation_bytes)
input_manifest = json.loads((generation / 'input-manifest.json').read_text())
generator_manifest = json.loads((generation / 'generator-manifest.json').read_text())
audit = json.loads(Path('/audit-input.json').read_text())['resolution']

classification = {
    entry['source_rule_id']: entry['classification']
    for entry in discovery['rules']
}
domain_rules = [
    rule for rule in inventory['rules']
    if classification[rule['source_rule_id']] == 'DOMAIN_LEMMA'
]
domain_ids = [rule['source_rule_id'] for rule in domain_rules]
obligations = obligation_map['obligations']
obligation_ids = [entry['source_rule_id'] for entry in obligations]

parsed_target = producer.target_statement(generated)
expected_definition = producer.expected_target_definition(obligation_map)
expected_definition_hash = producer.sha256_text(expected_definition)

checks = {
    'domain_rule_count': len(domain_rules),
    'obligation_count': len(obligations),
    'obligation_ids_unique': len(obligation_ids) == len(set(obligation_ids)),
    'ordered_domain_obligation_bijection': domain_ids == obligation_ids,
    'obligation_map_sha256': hashlib.sha256(obligation_bytes).hexdigest(),
    'obligation_map_hash_matches_manifest': hashlib.sha256(obligation_bytes).hexdigest() == generator_manifest['obligation_map_sha256'],
    'expected_target_definition_sha256': expected_definition_hash,
    'expected_target_hash_matches_manifest': expected_definition_hash == generator_manifest['target']['definition_sha256'],
    'parsed_target_equals_manifest': parsed_target == generator_manifest['target'],
    'parsed_target_equals_audit_input': parsed_target == audit['target'],
    'input_manifest_inventory_hash_matches': input_manifest['inventory_sha256'] == inventory['inventory_sha256'],
    'input_manifest_source_rules_equal_map': input_manifest['source_rules'] == obligation_map['source_rules'],
    'generator_obligation_count_matches': generator_manifest['obligation_count'] == len(obligations),
}

per_obligation = []
inventory_by_id = {rule['source_rule_id']: rule for rule in inventory['rules']}
for entry in obligations:
    rule = inventory_by_id[entry['source_rule_id']]
    per_obligation.append({
        'source_rule_id': entry['source_rule_id'],
        'source_span_matches': entry['source_span'] == {
            'start_line': rule['start_line'],
            'end_line': rule['end_line'],
        },
        'normalized_hash_matches': entry['normalized_sha256'] == rule['normalized_sha256'],
        'inventory_hash_matches': entry['inventory_sha256'] == inventory['inventory_sha256'],
        'discovery_hash_matches': entry['discovery_manifest_sha256'] == hashlib.sha256(discovery_bytes).hexdigest(),
        'conjunct_hash_matches': entry['lean_conjunct_sha256'] == hashlib.sha256(entry['lean_conjunct'].encode()).hexdigest(),
        'classification': classification[entry['source_rule_id']],
        'source_text': rule['text'],
        'lean_conjunct': entry['lean_conjunct'],
    })

checks['all_obligation_provenance_checks'] = all(
    all(item[key] for key in (
        'source_span_matches',
        'normalized_hash_matches',
        'inventory_hash_matches',
        'discovery_hash_matches',
        'conjunct_hash_matches',
    ))
    for item in per_obligation
)

print('STAGE 4 STRUCTURAL CHECKS')
print(json.dumps(checks, indent=2, sort_keys=True))
print('PER-OBLIGATION SOURCE/LEAN PAIRS')
print(json.dumps(per_obligation, indent=2, sort_keys=True))
print('EXPECTED FIXED TARGET DEFINITION')
print(expected_definition)
print('PARSED TARGET')
print(json.dumps(parsed_target, indent=2, sort_keys=True))

if not all(value for key, value in checks.items() if isinstance(value, bool)):
    raise SystemExit('Stage 4 structural check failed')
