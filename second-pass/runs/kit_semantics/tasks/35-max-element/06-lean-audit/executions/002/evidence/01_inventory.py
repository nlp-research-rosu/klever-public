#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification

workspace = Path('/reference/k-proof')
discovery_path = Path('/reference/lemma-discovery.json')
inventory = inventory_verification(workspace)
discovery_bytes = discovery_path.read_bytes()
discovery = json.loads(discovery_bytes)

inventory_rules = inventory['rules']
discovery_rules = discovery['rules']
inventory_ids = [entry['source_rule_id'] for entry in inventory_rules]
discovery_ids = [entry['source_rule_id'] for entry in discovery_rules]

print('RECONSTRUCTED INVENTORY')
print(json.dumps(inventory, indent=2, sort_keys=True))
print('BIJECTION AND HASH CHECKS')
checks = {
    'recomputed_inventory_sha256': canonical_json_sha256(inventory_rules),
    'inventory_self_hash_matches': inventory['inventory_sha256'] == canonical_json_sha256(inventory_rules),
    'discovery_inventory_hash': discovery.get('inventory_sha256'),
    'inventory_hash_matches_discovery': inventory['inventory_sha256'] == discovery.get('inventory_sha256'),
    'inventory_rule_count': len(inventory_rules),
    'discovery_rule_count': len(discovery_rules),
    'inventory_ids_unique': len(inventory_ids) == len(set(inventory_ids)),
    'discovery_ids_unique': len(discovery_ids) == len(set(discovery_ids)),
    'ordered_ids_equal': inventory_ids == discovery_ids,
    'missing_from_discovery': sorted(set(inventory_ids) - set(discovery_ids)),
    'extra_in_discovery': sorted(set(discovery_ids) - set(inventory_ids)),
    'discovery_file_sha256': hashlib.sha256(discovery_bytes).hexdigest(),
}
print(json.dumps(checks, indent=2, sort_keys=True))
print('ORDERED CLASSIFICATION TABLE')
by_id = {entry['source_rule_id']: entry for entry in discovery_rules}
for index, rule in enumerate(inventory_rules, 1):
    classified = by_id.get(rule['source_rule_id'], {})
    normalized = ' '.join(rule['text'].split())
    normalized_hash = hashlib.sha256(normalized.encode()).hexdigest()
    print(json.dumps({
        'index': index,
        'source_rule_id': rule['source_rule_id'],
        'module': rule['module'],
        'source_span': [rule['start_line'], rule['end_line']],
        'attributes': rule['attributes'],
        'normalized_sha256': rule['normalized_sha256'],
        'independent_normalized_sha256': normalized_hash,
        'id_matches_hash': rule['source_rule_id'] == 'rule-' + normalized_hash,
        'classification': classified.get('classification'),
        'rationale': classified.get('rationale'),
        'text': rule['text'],
    }, sort_keys=True))

if not all([
    checks['inventory_self_hash_matches'],
    checks['inventory_hash_matches_discovery'],
    checks['inventory_ids_unique'],
    checks['discovery_ids_unique'],
    checks['ordered_ids_equal'],
    not checks['missing_from_discovery'],
    not checks['extra_in_discovery'],
]):
    raise SystemExit('inventory comparison failed')
