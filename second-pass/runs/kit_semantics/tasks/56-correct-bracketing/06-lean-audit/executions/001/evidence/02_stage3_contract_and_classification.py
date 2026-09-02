#!/usr/bin/env python3
import json
from pathlib import Path

from tools.lemma_discovery_contract import validate_trust_boundary

workspace = Path('/reference/k-proof')
manifest = Path('/reference/lemma-discovery.json')
validated = validate_trust_boundary(workspace, manifest)

print('COMMAND: validate_trust_boundary(/reference/k-proof, /reference/lemma-discovery.json)')
print(json.dumps({
    'schema_version': validated['schema_version'],
    'verification_module': validated['verification_module'],
    'verification_modules': validated['verification_modules'],
    'inventory_sha256': validated['inventory_sha256'],
    'rule_count': len(validated['rules']),
    'definition_count': len(validated['definitions']),
    'operational_rule_count': len(validated['operational_rules']),
    'proved_derived_lemma_count': len(validated['proved_derived_lemmas']),
    'domain_lemma_count': len(validated['domain_lemmas']),
}, indent=2, sort_keys=True))

print('\nCOMMAND: display each frozen rule with attributes and protected classification')
by_id = {r['source_rule_id']: r for r in validated['rules']}
for entry in json.loads(manifest.read_text())['rules']:
    rule = by_id[entry['source_rule_id']]
    print(json.dumps({
        'source_rule_id': rule['source_rule_id'],
        'span': [rule['start_line'], rule['end_line']],
        'attributes': rule['attributes'],
        'classification': entry['classification'],
        'text': rule['text'],
        'rationale': entry['rationale'],
    }, sort_keys=True))
print('STAGE3_STRUCTURAL_CONTRACT: PASS')
