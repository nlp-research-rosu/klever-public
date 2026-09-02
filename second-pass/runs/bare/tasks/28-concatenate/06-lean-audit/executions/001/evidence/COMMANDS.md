# Audit command index

The numbered `.txt` files in this directory are raw `script(1)` captures unless
otherwise noted. `28_check_generation_returned_evidence.json` is the exact JSON
returned by the final trusted preflight run.

## Canonical inventory

```sh
PYTHONPATH=/reference python -c 'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'
```

Result: `03_reconstructed_rule_inventory.txt`.

The ordered identity, duplicate, omission, extra-entry, hash, and trust-boundary
comparison was run with `inventory_verification`,
`lemma_discovery_contract.validate_trust_boundary`, and the two ordered
`source_rule_id` lists. Result: `10_stage3_bijection_and_contract.txt`.

## Producer provenance

```sh
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json
```

```sh
PYTHONPATH=/reference python -c 'import json; from pathlib import Path; from tools.pipeline_contract import sha256_tree; p=Path("/reference/generation-tools"); expected=json.loads(Path("/audit-input.json").read_text())["resolution"]["hashes"]["generation_producer_sources_sha256"]; actual=sha256_tree(p); print(f"pipeline_contract.sha256_tree={actual}"); print(f"audit_input.expected={expected}"); print(f"match={actual == expected}")'
```

Results: `06_producer_source_hashes_and_references.txt`,
`07_producer_provenance_comparison.txt`, and
`09_launcher_producer_tree_hash.txt`.

## Trusted Stage 4 preflight

The initial exact call was:

```sh
PYTHONPATH=/reference python -c 'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"),Path("/reference/lemma-discovery.json"),Path("/reference/klean-generation"),toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result,indent=2,sort_keys=True))'
```

It failed before compilation because Lean/Lake could not resolve their
executables through the audit PID namespace. Result:
`11_fresh_check_generation.txt`.

After diagnosing the procfs/PID mismatch, the same call was rerun with only
this environment repair:

```sh
env \
  LD_PRELOAD=/tmp/audit-work/lean_pid_namespace_fix.so \
  PYTHONPATH=/reference \
  python -c 'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"),Path("/reference/lemma-discovery.json"),Path("/reference/klean-generation"),toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result,indent=2,sort_keys=True))'
```

Results: `22_fresh_check_generation_pass.txt` and the exact returned document
`28_check_generation_returned_evidence.json`. The repair source is preserved as
`lean_pid_namespace_fix.c`; its build and diagnostic outputs are in files
`12` through `21`.

## Independent hash and target checks

All launcher resolution hashes, per-file Stage 1 hashes, and the canonical
resolved-input hash were recomputed with the same trusted hash primitives.
Result: `24_audit_input_hash_recomputation.txt`.

The hash-verified generation-time `klean_export.py` was loaded directly and used
to recompute the Stage 1/export tree hashes, generated tree hash, eligible
source-rule list, expected target definition, and actual target statement.
These were compared with `input-manifest.json`, `generator-manifest.json`,
`export-result.json`, `obligation-map.json`, and `/audit-input.json`. Result:
`27_independent_stage4_bijection_and_target.txt`.

The generated target/proof-token search and Stage 5 candidate absence check are
in `25_generated_target_and_candidate_absence.txt`.
