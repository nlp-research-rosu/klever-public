#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract

audit = json.loads(Path('/audit-input.json').read_text())
resolution = audit['resolution']
expected = resolution['hashes']

observed = {
    'k_workspace_sha256': pipeline_contract.sha256_tree(Path('/reference/k-proof')),
    'stage1_export_sha256': klean_export.tree_digest(Path('/reference/k-proof')),
    'discovery_manifest_sha256': pipeline_contract.sha256_file(Path('/reference/lemma-discovery.json')),
    'k_audit_sha256': pipeline_contract.sha256_tree(Path('/reference/k-audit')),
    'klean_generation_sha256': pipeline_contract.sha256_tree(Path('/reference/klean-generation')),
    'generation_producer_sources_sha256': pipeline_contract.sha256_tree(Path('/reference/generation-tools')),
    'generated_tree_sha256': klean_export.tree_digest(Path('/reference/klean-generation/generated')),
    'lean_workspace_sha256': pipeline_contract.sha256_tree(Path('/candidate')),
}

print('AUDIT-INPUT TREE AND FILE HASHES')
for name, digest in observed.items():
    print(json.dumps({
        'name': name,
        'expected': expected.get(name),
        'observed': digest,
        'match': digest == expected.get(name),
    }, sort_keys=True))

source_hashes = resolution['stage1_source_hashes']
mismatches = []
missing = []
for relative, wanted in source_hashes.items():
    path = Path('/reference/k-proof') / relative
    if not path.is_file() or path.is_symlink():
        missing.append(relative)
        continue
    got = hashlib.sha256(path.read_bytes()).hexdigest()
    if got != wanted:
        mismatches.append({'path': relative, 'expected': wanted, 'observed': got})

print('STAGE1 SOURCE HASH TABLE SUMMARY')
print(json.dumps({
    'recorded_count': len(source_hashes),
    'missing_count': len(missing),
    'mismatch_count': len(mismatches),
    'missing': missing,
    'mismatches': mismatches,
}, indent=2, sort_keys=True))

unmounted = {
    'lean_invocation_sha256': {
        'expected': expected.get('lean_invocation_sha256'),
        'observed': None,
        'reason': 'The Stage 5 invocation directory is recorded but is not one of the mounted audit inputs.',
    },
}
print('UNMOUNTED RECORDED TREE')
print(json.dumps(unmounted, indent=2, sort_keys=True))

if not all(observed[name] == expected.get(name) for name in observed):
    raise SystemExit('an accessible audit-input hash mismatched')
if missing or mismatches:
    raise SystemExit('a recorded Stage 1 source hash mismatched')
