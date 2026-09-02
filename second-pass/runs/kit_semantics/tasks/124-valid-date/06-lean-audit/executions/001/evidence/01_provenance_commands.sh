#!/usr/bin/env bash
set -euo pipefail

printf 'AUDIT_MODE=%s\n' "${AUDIT_MODE-<unset>}"
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py
python3 -m json.tool /reference/generation-tools/source-manifest.json
python3 -m json.tool /reference/klean-generation/generator-manifest.json

PYTHONPATH=/reference python3 - <<'PY'
import hashlib
import json
from pathlib import Path

from tools.klean_audit_contract import _stage1_source_hashes
from tools.klean_export import tree_digest
from tools.pipeline_contract import sha256_tree
from tools.stage6_resolution_contract import (
    canonical_json_sha256,
    verify_audit_input,
)

audit = json.loads(Path('/audit-input.json').read_text())
resolution = audit['resolution']
recorded = resolution['hashes']

artifact_paths = {
    'generation_producer_sources_sha256': Path('/reference/generation-tools'),
    'k_workspace_sha256': Path('/reference/k-proof'),
    'k_audit_sha256': Path('/reference/k-audit'),
    'klean_generation_sha256': Path('/reference/klean-generation'),
}
observed = {key: sha256_tree(path) for key, path in artifact_paths.items()}
observed['stage1_export_sha256'] = tree_digest(Path('/reference/k-proof'))
observed['generated_tree_sha256'] = tree_digest(
    Path('/reference/klean-generation/generated')
)
observed['discovery_manifest_sha256'] = hashlib.sha256(
    Path('/reference/lemma-discovery.json').read_bytes()
).hexdigest()

print(json.dumps({
    'recorded_hashes': recorded,
    'observed_hashes': observed,
    'all_nonlean_recorded_hashes_match': all(
        observed[key] == recorded[key] for key in observed
    ),
}, indent=2, sort_keys=True))

expected_sources = resolution['stage1_source_hashes']
observed_sources = _stage1_source_hashes(Path('/reference/k-proof'))
print(json.dumps({
    'recorded_stage1_source_count': len(expected_sources),
    'observed_stage1_source_count': len(observed_sources),
    'stage1_source_hashes_match': expected_sources == observed_sources,
    'missing': sorted(set(expected_sources) - set(observed_sources)),
    'extra': sorted(set(observed_sources) - set(expected_sources)),
    'mismatched': sorted(
        key for key in expected_sources.keys() & observed_sources.keys()
        if expected_sources[key] != observed_sources[key]
    ),
}, indent=2, sort_keys=True))

verified_resolution, verified_digest = verify_audit_input(audit)
print(json.dumps({
    'audit_input_verified': verified_resolution == resolution,
    'recorded_resolved_input_sha256': audit['resolved_input_sha256'],
    'recomputed_resolved_input_sha256': canonical_json_sha256(resolution),
    'verified_resolved_input_sha256': verified_digest,
}, indent=2, sort_keys=True))
PY
