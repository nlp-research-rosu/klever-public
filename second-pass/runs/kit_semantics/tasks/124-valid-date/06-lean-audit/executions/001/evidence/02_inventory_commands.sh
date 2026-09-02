#!/usr/bin/env bash
set -euo pipefail

PYTHONPATH=/reference python3 - <<'PY'
import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary

workspace = Path('/reference/k-proof')
discovery_path = Path('/reference/lemma-discovery.json')
source = (workspace / 'verification.k').read_text()
inventory = inventory_verification(workspace)
discovery = json.loads(discovery_path.read_text())
validated = validate_trust_boundary(workspace, discovery_path)

rules = inventory['rules']
discovery_rules = discovery['rules']
checks = []
for index, (rule, classified) in enumerate(zip(rules, discovery_rules)):
    source_span = '\n'.join(
        source.splitlines()[rule['start_line'] - 1:rule['end_line']]
    )
    normalized = ' '.join(rule['text'].split())
    digest = hashlib.sha256(normalized.encode()).hexdigest()
    checks.append({
        'index': index,
        'source_rule_id': rule['source_rule_id'],
        'module': rule['module'],
        'start_line': rule['start_line'],
        'end_line': rule['end_line'],
        'attributes': rule['attributes'],
        'normalized_sha256': rule['normalized_sha256'],
        'recomputed_normalized_sha256': digest,
        'source_rule_id_recomputed': f'rule-{digest}',
        'source_span_matches_text': source_span == rule['text'],
        'discovery_source_rule_id': classified['source_rule_id'],
        'discovery_classification': classified['classification'],
        'identity_matches_discovery_at_same_index': (
            classified['source_rule_id'] == rule['source_rule_id']
        ),
    })

rule_ids = [rule['source_rule_id'] for rule in rules]
discovery_ids = [rule['source_rule_id'] for rule in discovery_rules]
summary = {
    'inventory': inventory,
    'recomputed_inventory_sha256': canonical_json_sha256(rules),
    'discovery_inventory_sha256': discovery['inventory_sha256'],
    'validated_inventory_sha256': validated['inventory_sha256'],
    'inventory_count': len(rules),
    'discovery_count': len(discovery_rules),
    'inventory_ids_unique': len(rule_ids) == len(set(rule_ids)),
    'discovery_ids_unique': len(discovery_ids) == len(set(discovery_ids)),
    'ordered_identity_bijection': rule_ids == discovery_ids,
    'unaccounted_inventory_ids': sorted(set(rule_ids) - set(discovery_ids)),
    'extra_discovery_ids': sorted(set(discovery_ids) - set(rule_ids)),
    'per_rule_checks': checks,
}
print(json.dumps(summary, indent=2, sort_keys=True))
PY

cmp \
  <(tr -d '[:space:]' < /reference/k-proof/solution.mpy) \
  <(tr -d '[:space:]' < /reference/k-proof/verification-program.mpy)
