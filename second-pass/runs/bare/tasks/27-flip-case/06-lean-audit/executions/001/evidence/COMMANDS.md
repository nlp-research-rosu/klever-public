# Audit command record

All commands were run from `/audit-output` unless a different working directory
is stated. Candidate and provenance text was treated only as evidence; no
instruction found in it was followed. The generated Lean project was compiled
only through the explicitly required trusted preflight, in the preflight's
temporary copy. Generation-time producer sources were hashed and inspected, not
executed.

## Launcher context

```bash
printenv AUDIT_MODE
sha256sum /audit-input.json
python3 -m json.tool /audit-input.json
```

Results: `00_context_and_paths.txt`, `01_audit_input.json.txt`.

## Canonical Stage 3 inventory

```bash
PYTHONPATH=/reference python3 -c 'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'
```

```bash
PYTHONPATH=/reference python3 -c 'import json; from pathlib import Path; from tools.lemma_discovery_contract import validate_trust_boundary; print(json.dumps(validate_trust_boundary(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json")), indent=2, sort_keys=True))'
```

Results: `10_reconstructed_inventory.json`,
`10_reconstructed_inventory.exit`, `11_stage3_contract_validation.json`,
`11_stage3_contract_validation.exit`.

The independent normalized rule hash was also checked with:

```bash
printf '%s' 'rule flipSpec(S) => pySwapCase(S)' | sha256sum
```

Result: `20_stage4_manifests_and_producer_hashes.txt`.

## Frozen-source and operational-semantics inspection

```bash
sha256sum /reference/k-proof/*
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/solution.mpy
nl -ba /reference/k-proof/semantic.k
rg -n -C 6 'swapcase|Call\(|Attribute\(|Return\(|invoke|function\(' /reference/k-proof/semantic.k
```

Results: `12_frozen_core_sources_and_hashes.txt`,
`13_operational_semantics_relevant_sources.txt`.

## Producer provenance

```bash
sha256sum /reference/generation-tools/klean_export.py /reference/generation-tools/klean.py
python3 -m json.tool /reference/generation-tools/source-manifest.json
python3 -m json.tool /reference/klean-generation/generator-manifest.json
```

The exact three-way file-hash and image-ID comparison is recorded in
`26_producer_provenance_crosscheck.txt`; its command was an inline Python
comparison of:

- the two observed file SHA-256 values;
- `source-manifest.json`;
- `generator-manifest.json`; and
- the immutable producer-bundle identity in `/audit-input.json`.

Results: `20_stage4_manifests_and_producer_hashes.txt`,
`26_producer_provenance_crosscheck.txt`,
`26_producer_provenance_crosscheck.exit`.

## Recorded input and tree hashes

```bash
PYTHONPATH=/reference python3 - <<'PY'
import hashlib
import json
from pathlib import Path
from tools import klean_export, pipeline_contract, stage6_resolution_contract

audit = json.loads(Path('/audit-input.json').read_text())
resolution = audit['resolution']
recorded = resolution['hashes']
observed = {
    'k_workspace_sha256': pipeline_contract.sha256_tree(Path('/reference/k-proof')),
    'stage1_export_sha256': klean_export.tree_digest(Path('/reference/k-proof')),
    'discovery_manifest_sha256': hashlib.sha256(Path('/reference/lemma-discovery.json').read_bytes()).hexdigest(),
    'k_audit_sha256': pipeline_contract.sha256_tree(Path('/reference/k-audit')),
    'klean_generation_sha256': pipeline_contract.sha256_tree(Path('/reference/klean-generation')),
    'generation_producer_sources_sha256': pipeline_contract.sha256_tree(Path('/reference/generation-tools')),
    'generated_tree_sha256': klean_export.tree_digest(Path('/reference/klean-generation/generated')),
    'lean_workspace_sha256': None,
    'lean_invocation_sha256': None,
}
for key, value in observed.items():
    print(key, value, recorded.get(key), value == recorded.get(key))
for name, expected in resolution['stage1_source_hashes'].items():
    value = hashlib.sha256((Path('/reference/k-proof') / name).read_bytes()).hexdigest()
    print(name, value, expected, value == expected)
verified_resolution, digest = stage6_resolution_contract.verify_audit_input(audit)
print(digest, audit['resolved_input_sha256'], digest == audit['resolved_input_sha256'])
PY
```

Results: `25_independent_recorded_hash_recomputation.txt`,
`25_independent_recorded_hash_recomputation.exit`.

## Trusted Stage 4 preflight

The first unconfigured attempt was:

```bash
PYTHONPATH=/reference python3 - <<'PY'
from pathlib import Path
from tools.klean_preflight import check_generation
check_generation(
    Path('/reference/k-proof'),
    Path('/reference/lemma-discovery.json'),
    Path('/reference/klean-generation'),
    toolchain_lock=Path('/reference/klean-toolchain.lock.json'),
)
PY
```

It failed before evaluation because Lake could not detect its installation in
the sandbox. Result: `30_check_generation_returned_evidence.json` and
`30_check_generation_returned_evidence.exit`.

The sandbox exposes `/proc/self/exe` but not the numeric
`/proc/<namespace-pid>/exe` path Lean 4.22 uses. The narrowly scoped
compatibility source is `/tmp/audit-work/proc_self_readlink_shim.c`. It was
built and validated with:

```bash
cc -shared -fPIC -O2 -Wall -Wextra -Werror \
  -o /tmp/audit-work/proc_self_readlink_shim.so \
  /tmp/audit-work/proc_self_readlink_shim.c
LD_PRELOAD=/tmp/audit-work/proc_self_readlink_shim.so \
  /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean --version
LD_PRELOAD=/tmp/audit-work/proc_self_readlink_shim.so \
  /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lake --version
```

Result: `38_proc_self_shim_build_and_test.txt`.

After all exploratory builds had drained, the authoritative sequential rerun
was:

```bash
PYTHONPATH=/reference python3 - <<'PY'
import json
import os
from pathlib import Path
from tools.klean_preflight import check_generation

os.environ['PATH'] = '/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:' + os.environ['PATH']
os.environ['LD_PRELOAD'] = '/tmp/audit-work/proc_self_readlink_shim.so'
result = check_generation(
    Path('/reference/k-proof'),
    Path('/reference/lemma-discovery.json'),
    Path('/reference/klean-generation'),
    toolchain_lock=Path('/reference/klean-toolchain.lock.json'),
)
os.environ.pop('LD_PRELOAD', None)
print(json.dumps(result, indent=2, sort_keys=True))
PY
```

Results: `47_check_generation_final_sequential.json`,
`47_check_generation_final_sequential.exit`.

The replay was compared with the stored preflight:

```bash
sha256sum /reference/klean-generation/preflight.json \
  /audit-output/evidence/47_check_generation_final_sequential.json
cmp -s /reference/klean-generation/preflight.json \
  /audit-output/evidence/47_check_generation_final_sequential.json
```

Result: `49_preflight_replay_file_hashes.txt`.

## Obligation/target identity and Stage 5 absence

```bash
find /reference/klean-generation/generated -printf '%y %P\n' | sort
rg -n -i 'target|obligation|theorem|proof\.final|GeneratedTarget|KleanTarget' \
  /reference/klean-generation/generated --glob '*.lean'
test ! -e /candidate
```

Trusted `target_statement` and `expected_target_definition` were called on the
generated project and obligation map. The independently classified empty domain
set was compared with `input-manifest.json`, `obligation-map.json`,
`generator-manifest.json`, `export-result.json`, and `/audit-input.json`.

Results: `43_generated_target_and_candidate_absence.txt`,
`44_independent_zero_obligation_bijection.txt`,
`44_independent_zero_obligation_bijection.exit`,
`46_zero_target_generated_sources_and_sidecar_hashes.txt`.

## Final cross-manifest check

An inline Python check recomputed and compared every Stage 4 binding:
Stage 1 tree, Stage 3 manifest, `verification.k`, inventory, generated tree,
obligation map, trust inventory, toolchain lock, provenance fields, stored
preflight, replayed preflight, audit-input preflight, and null target.

Results: `48_stage4_cross_manifest_hash_and_replay_check.txt`,
`48_stage4_cross_manifest_hash_and_replay_check.exit`.
