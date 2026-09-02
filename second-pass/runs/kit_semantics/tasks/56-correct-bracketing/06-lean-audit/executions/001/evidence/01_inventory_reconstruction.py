#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification

workspace = Path('/reference/k-proof')
verification_path = workspace / 'verification.k'
manifest_path = Path('/reference/lemma-discovery.json')
verification = verification_path.read_text()
manifest = json.loads(manifest_path.read_text())
inventory = inventory_verification(workspace)

print('COMMAND: inventory_verification(Path("/reference/k-proof")) using /reference/tools/k_rule_inventory.py')
print(json.dumps(inventory, indent=2, sort_keys=True))

print('\nCOMMAND: independently check spans, normalized hashes, source_rule_ids, order, uniqueness, and whole inventory hash')
lines = verification.splitlines()
checks = []
for index, rule in enumerate(inventory['rules']):
    source_slice = '\n'.join(lines[rule['start_line'] - 1:rule['end_line']])
    normalized = ' '.join(rule['text'].split())
    digest = hashlib.sha256(normalized.encode()).hexdigest()
    row = {
        'index': index,
        'module': rule['module'],
        'span': [rule['start_line'], rule['end_line']],
        'source_rule_id': rule['source_rule_id'],
        'text_matches_source_span': source_slice == rule['text'],
        'normalized_sha256_recomputed': digest,
        'normalized_hash_matches': digest == rule['normalized_sha256'],
        'source_rule_id_matches': rule['source_rule_id'] == f'rule-{digest}',
    }
    checks.append(row)
    print(json.dumps(row, sort_keys=True))

manual_inventory_hash = hashlib.sha256(json.dumps(
    inventory['rules'], sort_keys=True, separators=(',', ':'), ensure_ascii=False
).encode()).hexdigest()
print(f'manual_inventory_sha256={manual_inventory_hash}')
print(f'trusted_canonical_json_sha256={canonical_json_sha256(inventory["rules"])}')
print(f'inventory_reported_sha256={inventory["inventory_sha256"]}')

canonical_ids = [r['source_rule_id'] for r in inventory['rules']]
manifest_ids = [r['source_rule_id'] for r in manifest['rules']]
comparison = {
    'canonical_rule_count': len(canonical_ids),
    'manifest_rule_count': len(manifest_ids),
    'canonical_ids_unique': len(canonical_ids) == len(set(canonical_ids)),
    'manifest_ids_unique': len(manifest_ids) == len(set(manifest_ids)),
    'ordered_identity_equal': manifest_ids == canonical_ids,
    'identity_sets_equal': set(manifest_ids) == set(canonical_ids),
    'manifest_inventory_hash_equal': manifest.get('inventory_sha256') == inventory['inventory_sha256'],
    'verification_sha256_recomputed': hashlib.sha256(verification_path.read_bytes()).hexdigest(),
    'all_span_and_rule_hash_checks': all(
        r['text_matches_source_span'] and r['normalized_hash_matches'] and r['source_rule_id_matches']
        for r in checks
    ),
}
print(json.dumps(comparison, indent=2, sort_keys=True))
if not all(value for key, value in comparison.items() if not key.endswith('_count') and key != 'verification_sha256_recomputed'):
    raise SystemExit('INVENTORY_BIJECTION_FAILED')
print('INVENTORY_BIJECTION: PASS')
